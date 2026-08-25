# frozen_string_literal: true

require "json"

source = File.read(File.expand_path("../404.html", __dir__))

reels_json = source[/var REELS = (\[.*?\]);\n  var LABELS/m, 1]
abort "Could not find the 404 reel strips" unless reels_json

reels = JSON.parse(reels_json)

def payout_map(source, pattern, label)
  body = source[pattern, 1]
  abort "Could not find #{label}" unless body

  body.scan(/(\w+):\s*(\d+)/).to_h.transform_values(&:to_i)
end

triples = payout_map(source, /var THREE_KIND = \{(.*?)\};/m, "triple payouts")
pairs = payout_map(source, /var pairPays = \{(.*?)\};/m, "pair payouts")

hits = 0
paid = 0

reels[0].product(reels[1], reels[2]).each do |faces|
  prize = if faces == %w[four zero four]
            0
          elsif faces.uniq.length == 1
            triples.fetch(faces.first)
          else
            pair = pairs.find { |face, _| faces.count(face) == 2 }
            pair ? pair.last : 0
          end

  hits += 1 if prize.positive?
  paid += prize
end

total = reels.map(&:length).inject(:*)
expected = { combinations: 13_824, hits: 4_571, paid: 13_174 }
actual = { combinations: total, hits: hits, paid: paid }

abort "404 slot odds changed: expected #{expected}, got #{actual}" unless actual == expected
abort "Visible BAR payout does not match the game" unless source.include?("<span>BAR BAR BAR</span><b>$#{triples.fetch('bar')}</b>")

hit_rate = hits.fdiv(total) * 100
return_rate = paid.fdiv(total) * 100

abort "Documented hit frequency is stale" unless source.include?(format("%.7f%% hit frequency", hit_rate))
abort "Documented return is stale" unless source.include?(format("returns exactly %.7f%%", return_rate))

puts format("404 slot verified: %.7f%% hit frequency, %.7f%% return", hit_rate, return_rate)

require 'open-uri'
require 'nokogiri'

doc = Nokogiri::HTML(open(ARGV[0]).read)

title = doc.css("h1").text
items = doc.css("ul li").collect{|l| l.text.split(/\n/)[0]}.reject{|l| l =~ /\d/}



puts title
puts items.inspect

open("lists/#{title}.csv", "w"){|f| f << "#{title},#{items.join(",")}"}
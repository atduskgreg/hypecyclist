require 'wordnet'

@nounIndex = WordNet::NounIndex.instance
@adjIndex = WordNet::AdjectiveIndex.instance
@advIndex = WordNet::AdverbIndex.instance

# TODO: "technology" needs something special
terms = ["technology trigger", 
		 "peak of inflated expectation",
		 "trough of disillusionment",
		 "slope of enlightenment",
		 "plateau of productivity"]

term_labels = [[:noun, :noun],
			   [:noun, "of", :adj, :noun],
			   [:noun, "of", :noun],
			   [:noun, "of", :noun],
			   [:noun, "of", :noun]]

#w[0].synsets.collect(&:words).flatten.uniq - ["peak"]

def synonyms_for(word, pos)
	case pos
	when :noun
		index = @nounIndex.find(word)
		synonyms_from(index) - [word]
	when :adj
		index = @adjIndex.find(word)
		index.pos = "adj"
		synonyms_from(index) - [word]
	when :adv
		index = @advIndex.find(word)
		index.pos = "adv"
		synonyms_from(index) - [word]
	end
end

def synonyms_from(index)
	(index.synsets.collect(&:words) + index.synsets.collect(&:children).flatten.collect(&:words)).flatten.uniq 
end

terms.each_with_index do |t,i|
	phrase = []
	t.split(" ").each_with_index do |w,j|
		if w == "of"
			phrase << w
		else
			# puts w + "," + term_labels[j][i].to_s
			syns = synonyms_for(w,term_labels[j][i])
			if syns
				phrase << syns.sample.gsub("_", " ")
			else
				phrase << w
			end
		end
	end
	puts phrase.join(" ")
end
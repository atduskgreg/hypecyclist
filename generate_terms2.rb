require 'wordnet'

@nounIndex = WordNet::NounIndex.instance
@adjIndex = WordNet::AdjectiveIndex.instance
@advIndex = WordNet::AdverbIndex.instance

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

def one_synonym(arr, pos)
	s = arr.collect{|w| synonyms_for(w,pos)}.flatten.sample
	s.split(/_|\s/).collect{|w| w.capitalize}.join("\n")
end


case ARGV[0]

when "start"
	puts one_synonym(["start", "beginning", "birth"], :noun) + "\nof\n" + one_synonym(["innovation", "invention", "novelty"], :noun)
when "max"
	puts one_synonym(["peak", "crest", "pinnacle", "crown", "vertex"], :noun) + "\nof\n" + one_synonym(["inflated", "exaggerated", "farfetched"], :adj) + " " + one_synonym(["expectation", "prediction", "forecast"], :noun)
when "min"
	puts one_synonym(["minimum", "bottom", "trough", "depression"], :noun) + "\nof\n" + one_synonym(["disappointment", "disillusionment"], :noun)
when "slup" # slope up
	puts one_synonym(["ascent", "incline", "climb", "rise"], :noun) + "\nof\n" + one_synonym(["enlightenment", "knowledge", "invention"], :noun)
when "slown" # slope down
	puts one_synonym(["slope", "descent", "decline", "depth"], :noun) + "\nof\n" + one_synonym(["defeat", "setback", "discouragement"], :noun)
when "flat"
	puts one_synonym(["plateau", "expanse", "field", "plane", "flatine"], :noun) + "\nof\n" + one_synonym(["productivity", "capacity", "effectiveness"], :noun)
end

# terms = ["technology trigger", 
# 		 "peak of inflated expectation",
# 		 "trough of disillusionment",
# 		 "slope of enlightenment",
# 		 "plateau of productivity"]




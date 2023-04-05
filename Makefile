EXAMPLES=$(wildcard *.py)
.PHONY: $(EXAMPLES)

run-examples:: $(EXAMPLES)

$(EXAMPLES):
	sh -c "time ./$@"

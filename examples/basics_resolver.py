from tense import TenseParser, resolvers

complex_string = "1minute and 10 seconds + 5 seconds"

digit_parser = TenseParser(TenseParser.DIGIT)
assert digit_parser.parse(complex_string) != 75  # :C sad, but...

digit_parser.resolver = resolvers.smart_resolver  # <-----------------------|
assert digit_parser.parse(complex_string) == 75  # =) happy                 |
# or                                                                      # | equals
new_digit_parser = TenseParser(  # | to
    TenseParser.DIGIT,  # |
    time_resolver=resolvers.smart_resolver,  # <----------------------------|
)
assert new_digit_parser.parse(complex_string) == 75  # =) happy

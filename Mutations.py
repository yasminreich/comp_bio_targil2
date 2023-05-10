import Person, random
def switchMutation(person: Person) -> None:
    keys = list(person.getEncodingDict().keys())
    key1, key2 = random.sample(keys, 2)
    person.getEncodingDict()[key1], person.getEncodingDict()[key2] = person.getEncodingDict()[key2], person.getEncodingDict()[key1]
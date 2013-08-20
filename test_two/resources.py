# -*- coding: utf-8 -*-
import colander


todos = [
    {'id': 1, 'title': 'Get shit done …'},
    {'id': 2, 'title': 'Get more shit done …'},
    {'id': 3, 'title': 'Get even more shit done …'}
]

class Todo(colander.MappingSchema):
    id = colander.SchemaNode(colander.Int(), validator=colander.Range(2, 9999))
    title = colander.SchemaNode(colander.String(), validator=colander.Length(min=5))


todo = {'id': 1, 'title': 'hiho'}
schema = Todo()
serialized = schema.serialize(todo)

print str(serialized)
deserialized = schema.deserialize(serialized)
print str(deserialized)

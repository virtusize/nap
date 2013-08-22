# Use cases for the API

- Product creation (integrate measurement submission into third party systems)
- Statistics (track items flow from first look to return)
- More frontends, i. e. mobile/apps
- Decoupling webapps from the backend to make them more standalone. That would
  enable us to have dedicated product teams in the future or even outsource
  some development, like an iOS app or a bulk uploader to a third party.
- Automatic size charts, that are i18n


# Resources

These resources are defined using the JSON Siren notation for hypermedia. See [Siren](https://github.com/kevinswiber/siren).
This does not necessarily mean, that our API has to speak Siren. We could let it speak [HAL](http://stateless.co/hal_specification.html) or [Collection+JSON](http://amundsen.com/media-types/collection) instead.

##`User`

```json
{
    "class": ["User", "item"],
    "properties": {
        "name": "John",
        "email": "john@virtusize.com"
    },
    "entities": [
        {
            "class": ["UserProduct", "collection"],
            "rel": "http://api.virtusize.com/user-products",
            "href": "http://api.virtusize.com/users/1/user-products"
        }
    ],
    "actions": [
        {
            "name": "update",
            "title": "Update User",
            "method": "PATCH",
            "href": "http://api.virtusize.com/users/1",
            "type": "application/x-www-form-urlencoded",
            "fields": [
                {"name": "name", "type": "text"},
                {"name": "email", "type": "text"}
            ]
        }
    ],
    "links": [
        {"rel": ["self"], "href": "http://api.virtusize.com/users/1"}
    ]
}
```

##`UserProduct`

```json
{
    "class": ["UserProduct", "item"],
    "properties": {
        "name": "My favorite sweater"
    },
    "entities": [
        {
            "class": ["User", "item"],
            "rel": "http://api.virtusize.com/users",
            "href": "http://api.virtusize.com/user/1"
        },
        {
            "class": ["StoreProduct", "item"],
            "rel": "http://api.virtusize.com/store-products",
            "href": "http://api.virtusize.com/store-products/3"
        },
        {
            "class": ["SizeSet", "item"],
            "rel": "http://api.virtusize.com/size-sets",
            "href": "http://api.virtusize.com/size-sets/24"
        }
    ],
    "actions": [ ],
    "links": [
        {"rel": ["self"], "href": "http://api.virtusize.com/user-products/17"}
    ]
}
```

##`StoreProduct`

```json
{
    "class": ["StoreProduct", "item"],
    "properties": {
        "name": "Pink sweater",
        "externalId": "SKU1234567890"
    },
    "entities": [
        {
            "class": ["Store", "item"],
            "rel": "http://api.virtusize.com/stores",
            "href": "http://api.virtusize.com/stores/8"
        },
        {
            "class": ["SizeSet", "item"],
            "rel": "http://api.virtusize.com/size-sets",
            "href": "http://api.virtusize.com/size-sets/24"
        }
    ],
    "actions": [ ],
    "links": [
        {"rel": ["self"], "href": "http://api.virtusize.com/store-products/8"}
    ]
}
```

##`ProductType`

```json
{
    "class": ["ProductType", "item"],
    "properties": {
        "name": "dress"
        "requiredMeasurements": ["waist", "height", "bust"],
        "optionalMeasurements": ["hip", "sleeveOpening"],
        "maxMeasurements": {"waist": 900, "height": 1500, "bust": 750},
        "minMeasurements": {"waist": 400, "height": 1000, "bust": 350},
        "defaultMeasurements": {"waist": 650, "height": 1250, "bust": 500}
    },
    "entities": [ ],
    "actions": [ ],
    "links": [
        {"rel": ["self"], "href": "http://api.virtusize.com/product-types/1"}
    ]
}
```

##`SizeSet`

```json
{
    "class": ["SizeSet", "item"],
    "properties": {
        "sizes": {
            "Small": {"hip": 380, "waist": 330, "bust": 350, "height": 700},
            "Medium": {"hip": 400, "waist": 350, "bust": 370, "height": 720}, 
            "X-Small": {"hip": 360, "waist": 310, "bust": 330, "height": 680}
        }
    },
    "entities": [
        {
            "class": ["StoreProduct", "item"],
            "rel": "http://api.virtusize.com/store-products",
            "href": "http://api.virtusize.com/store-products/7"
        }
    ],
    "actions": [ ],
    "links": [
        {"rel": ["self"], "href": "http://api.virtusize.com/size-sets/4"}
    ]
}
```

##`Store`

```json
{
    "class": ["Store", "item"],
    "properties": {
        "name": "Massimo Dutti",
        "shortName": "massimo_dutti",
        "apiKey": "3d0f27de5681cc43733ee7dcc9fe3cb9351768fe"
    },
    "entities": [
        {
            "class": ["StoreProduct", "collection"],
            "rel": "http://api.virtusize.com/store-products",
            "href": "http://api.virtusize.com/stores/23/store-products"
        },
    ],
    "actions": [ ],
    "links": [
        {"rel": ["self"], "href": "http://api.virtusize.com/stores/23"}
    ]
}
```


##Errors
A nice example of an error response from http://youtu.be/hdSrT4yjS1g?t=59m36s

```
POST /directories
409 Conflict
```

```json
{
    "status": 409,
    "code": 40924,
    "property": "name",
    "message": "A directory named 'Avengers' already exists.",
    "developerMessage": "A directory named 'Avengers' already exists. If you
    have a stale local cache, please expire it now.",
    "moreInfo": "https://www.stormpath.com/docs/api/errors/40924"
}
```


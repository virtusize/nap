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

##`Product`

```json
{
    "class": ["Product", "item"],
    "properties": {
        "name": "Pink sweater",
        "ownerId": 88,
        "ownderType": "Brand"
    },
    "entities": [
        {
            "class": ["Brand", "item"],
            "rel": "http://api.virtusize.com/brands",
            "href": "http://api.virtusize.com/brands/3"
        },
        {
            "class": ["ProductType", "item"],
            "rel": "http://api.virtusize.com/product-types",
            "href": "http://api.virtusize.com/product-types/7"
        },
        {
            "class": ["MeasurementSet", "collection"],
            "rel": "http://api.virtusize.com/measurement-sets",
            "href": "http://api.virtusize.com/products/14/measurement-sets"
        },
        {
            "class": ["StoreProducts", "collection"],
            "rel": "http://api.virtusize.com/store-products",
            "href": "http://api.virtusize.com/products/14/store-products"
        },
        {
            "class": ["UserProducts", "collection"],
            "rel": "http://api.virtusize.com/user-products",
            "href": "http://api.virtusize.com/products/14/user-products"
        },
    ],
    "actions": [ ],
    "links": [
        {"rel": ["self"], "href": "http://api.virtusize.com/products/14"}
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
            "class": ["Product", "item"],
            "rel": "http://api.virtusize.com/products",
            "href": "http://api.virtusize.com/products/3"
        },
        {
            "class": ["MeasurementSet", "item"],
            "rel": "http://api.virtusize.com/measurement-sets",
            "href": "http://api.virtusize.com/measurement-sets/24"
        },
        {
            "class": ["Measurement", "collection"],
            "rel": "http://api.virtusize.com/measurements",
            "href": "http://api.virtusize.com/user-products/17/measurements"
        },
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
            "class": ["MeasurementSet", "collection"],
            "rel": "http://api.virtusize.com/measurement-sets",
            "href": "http://api.virtusize.com/store-products/8/measurement-sets"
        },
        {
            "class": ["Products", "item"],
            "rel": "http://api.virtusize.com/products",
            "href": "http://api.virtusize.com/products/3"
        },
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
    },
    "entities": [
        {
            "class": ["MeasurementTemplate", "collection"],
            "rel": "http://api.virtusize.com/measurement-templates",
            "href": "http://api.virtusize.com/product-types/1/measurement-templates"
        },
        {
            "class": ["Product", "collection"],
            "rel": "http://api.virtusize.com/products",
            "href": "http://api.virtusize.com/product-types/1/products"
        }
    ],
    "actions": [ ],
    "links": [
        {"rel": ["self"], "href": "http://api.virtusize.com/product-types/1"}
    ]
}
```

##`MeasurementTemplate`

```json
{
    "class": ["MeasurementTemplate", "item"],
    "properties": {
        "name": "height",
        "required": true,
        "arrow": true,
        "min": 500,
        "max": 1700,
        "default": 900
    },
    "entities": [
        {
            "class": ["ProductType", "item"],
            "rel": "http://api.virtusize.com/product-types",
            "href": "http://api.virtusize.com/product-types/1"
        },
        {
            "class": ["Measurement", "collection"],
            "rel": "http://api.virtusize.com/measurements",
            "href": "http://api.virtusize.com/measurement-templates/2/measurements"
        }
    ],
    "actions": [ ],
    "links": [
        {"rel": ["self"], "href": "http://api.virtusize.com/measurement-templates/2"}
    ]
}
```

##`Measurement`

```json
{
    "class": ["Measurement", "item"],
    "properties": {
        "name": "dress"
    },
    "entities": [
        {
            "class": ["Product", "item"],
            "rel": "http://api.virtusize.com/products",
            "href": "http://api.virtusize.com/products/11"
        },
        {
            "class": ["Measurement", "collection"],
            "rel": "http://api.virtusize.com/measurements",
            "href": "http://api.virtusize.com/measurement-templates/2/measurements"
        }
    ],
    "actions": [ ],
    "links": [
        {"rel": ["self"], "href": "http://api.virtusize.com/measurement-templates/2"}
    ]
}
```

##`MeasurementSet`

```json
{
    "class": ["MeasurementSet", "item"],
    "properties": {
        "position": 1
    },
    "entities": [
        {
            "class": ["Measurement", "collection"],
            "rel": "http://api.virtusize.com/measurements",
            "href": "http://api.virtusize.com/measurement-sets/4/measurements"
        },
        {
            "class": ["Product", "item"],
            "rel": "http://api.virtusize.com/products",
            "href": "http://api.virtusize.com/products/11"
        },
        {
            "class": ["RegionMeasurementSet", "collection"],
            "rel": "http://api.virtusize.com/region-measurement-sets",
            "href": "http://api.virtusize.com/measurement-sets/4/region-measurement-sets"
        },
        {
            "class": ["StoreProduct", "item"],
            "rel": "http://api.virtusize.com/store-products",
            "href": "http://api.virtusize.com/store-products/7"
        },
    ],
    "actions": [ ],
    "links": [
        {"rel": ["self"], "href": "http://api.virtusize.com/measurement-sets/4"}
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
            "class": ["RegionSet", "collection"],
            "rel": "http://api.virtusize.com/region-sets",
            "href": "http://api.virtusize.com/stores/23/region-sets"
        },
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

##`Brand` 

```json
{
    "class": ["Brand", "item"],
    "properties": {
        "name": "Diesel"
    },
    "entities": [
        {
            "class": ["Product", "collection"],
            "rel": "http://api.virtusize.com/products",
            "href": "http://api.virtusize.com/brands/17/products"
        }
    ],
    "actions": [ ],
    "links": [
        {"rel": ["self"], "href": "http://api.virtusize.com/brands/17"}
    ]
}
```

##`Region` 

```json
{
    "class": ["Region", "item"],
    "properties": {
        "name": "Great Britain",
        "code": "GB"
    },
    "entities": [
        {
            "class": ["RegionMeasurementSet", "collection"],
            "rel": "http://api.virtusize.com/region-measurement-sets",
            "href": "http://api.virtusize.com/regions/3/region-measurement-sets"
        },
        {
            "class": ["StoreRegion", "collection"],
            "rel": "http://api.virtusize.com/store-regions",
            "href": "http://api.virtusize.com/regions/3/store-regions"
        },
    ],
    "actions": [ ],
    "links": [
        {"rel": ["self"], "href": "http://api.virtusize.com/regions/3"}
    ]
}
```

##`StoreRegion`

```json
{
    "class": ["StoreRegion", "item"],
    "properties": {
        "default": true 
    },
    "entities": [
        {
            "class": ["Store", "item"],
            "rel": "http://api.virtusize.com/stores",
            "href": "http://api.virtusize.com/stores/8"
        },
        {
            "class": ["Region", "item"],
            "rel": "http://api.virtusize.com/regions",
            "href": "http://api.virtusize.com/regions/3"
        },
    ],
    "actions": [ ],
    "links": [
        {"rel": ["self"], "href": "http://api.virtusize.com/store-regions/6"}
    ]
}
```

##`MeasurementSetRegion` 

```json
{
    "class": ["MeasurementSetRegion", "item"],
    "properties": {
        "name": "38"
    },
    "entities": [
        {
            "class": ["Region", "item"],
            "rel": "http://api.virtusize.com/regions",
            "href": "http://api.virtusize.com/regions/3"
        },
        {
            "class": ["MeasurementSet", "item"],
            "rel": "http://api.virtusize.com/measurement-sets",
            "href": "http://api.virtusize.com/measurement-sets/42"
        },
    ],
    "actions": [ ],
    "links": [
        {"rel": ["self"], "href": "http://api.virtusize.com/measurement-set-regions/25"}
    ]
}
```






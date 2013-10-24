Nap Changes
==============

Instructions:
Use list notation, and following prefixes:

- Feature - for any new features
- Cleanup - any code removal or non visible maintenance change
- Refactor - code refactoring, keeping same functionality
- Bugfix - when fixing any major bug


### NEXT RELEASE

- Refactor: Moved flask.json stuff into nap.util. (hs)
- Feature: View filters now accept lists and filter on the containing elements. (hs)
- Refactor: Model class is now responsible for creating its name. (hs)
- Refactor: NapClients call method is now public for adding API custom routes. (hs)
- Feature: Added a method to find a view of the Api by endpoint prefix. (hs)
- Feature: Added blinker signals to SAModelController for create, update and delete actions. (hs)
- Feature: Now empty results get handled by authorization. For possible improvements see Github Issues. (hs)
- Feature: Added in process nap client and http client libraries. (hs)
- Refactor: Now errors that get transmitted as json use camelized keys. (hs)
- Feature: Added query as a default implemented controller and view method. (hs)
- Cleanup: Removed a print statement from caching_query. (hs)
- Minor: Added main python script to run the test API. (hs)

### 0.1.1

- Feature: Handling other exceptions by returning json responses (hs)


### 0.1.0

- Initial release!


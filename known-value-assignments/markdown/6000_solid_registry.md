# solid Known Values Registry

## Ontology Information

| Property | Value |
|----------|-------|
| **Name** | solid |
| **Source URL** | http://www.w3.org/ns/solid/terms# |
| **Start Code Point** | 6000 |
| **Processing Strategy** | StandardRDF |

## Statistics

| Metric | Value |
|--------|-------|
| **Total Entries** | 33 |
| **Code Point Range** | 6000 - 6032 |

## Entries

| Codepoint | Canonical Name | Type | URI | Description |
|-----------|----------------|------|-----|-------------|
| 6000 | `Account` | class | http://www.w3.org/ns/solid/terms#Account | A Solid account. |
| 6001 | `Inbox` | class | http://www.w3.org/ns/solid/terms#Inbox | A resource containing notifications. |
| 6002 | `insertdeletePatch` | class | http://www.w3.org/ns/solid/terms#InsertDeletePatch | A class of patch expressing insertions, deletions, and conditional modifications to a resource that has an RDF-based representation. |
| 6003 | `listedTypeIndex` | class | http://www.w3.org/ns/solid/terms#ListedDocument | Listed Type Index is a registry of resources that are publicly discoverable by outside users and applications. |
| 6004 | `Notification` | class | http://www.w3.org/ns/solid/terms#Notification | A notification resource. |
| 6005 | `Patch` | class | http://www.w3.org/ns/solid/terms#Patch | A patch expresses conditional modifications to a resource that has an RDF-based representation. |
| 6006 | `Timeline` | class | http://www.w3.org/ns/solid/terms#Timeline | A resource containing time ordered items and sub-containers.  Sub-containers may be desirable in file based systems to split the timeline into logical components e.g. /yyyy-mm-dd/ as used in ISO 8061. |
| 6007 | `typeIndex` | class | http://www.w3.org/ns/solid/terms#TypeIndex | A index of type registries for resources. Applications can register the RDF type they use and list them in the index resource. |
| 6008 | `typeRegistration` | class | http://www.w3.org/ns/solid/terms#TypeRegistration | The registered types that map a RDF classes/types to their locations using either `instance` or `instanceContainer` property. |
| 6009 | `unlistedTypeIndex` | class | http://www.w3.org/ns/solid/terms#UnlistedDocument | Unlisted Type Index is a registry of resources that are private to the user and their apps, for types that are not publicly discoverable. |
| 6010 | `account` | property | http://www.w3.org/ns/solid/terms#account | A solid account belonging to an Agent. |
| 6011 | `deletes` | property | http://www.w3.org/ns/solid/terms#deletes | The triple patterns this patch removes from the document. |
| 6012 | `registryClass` | property | http://www.w3.org/ns/solid/terms#forClass | A class that is used to map an listed or unlisted type index. |
| 6013 | `inboxDeprecated` | property | http://www.w3.org/ns/solid/terms#inbox | Deprecated pointer to a Linked Data Notifications inbox; please use http://www.w3.org/ns/ldp#inbox instead. |
| 6014 | `inserts` | property | http://www.w3.org/ns/solid/terms#inserts | The triple patterns this patch adds to the document. |
| 6015 | `instance` | property | http://www.w3.org/ns/solid/terms#instance | Maps a type to an individual resource, typically an index or a directory listing resource. |
| 6016 | `instanceContainer` | property | http://www.w3.org/ns/solid/terms#instanceContainer | Maps a type to a container which the client would have to list to get the instances of that type. |
| 6017 | `loginEndpoint` | property | http://www.w3.org/ns/solid/terms#loginEndpoint | The login URI of a given server. |
| 6018 | `logoutEndpoint` | property | http://www.w3.org/ns/solid/terms#logoutEndpoint | The logout URI of a given server. |
| 6019 | `notification` | property | http://www.w3.org/ns/solid/terms#notification | Notification resource for an inbox. |
| 6020 | `oidcIssuer` | property | http://www.w3.org/ns/solid/terms#oidcIssuer | The preferred OpenID Connect issuer URI for a given WebID. |
| 6021 | `owner` | property | http://www.w3.org/ns/solid/terms#owner | A person or social entity that is considered to have control, rights, and responsibilities over a data storage. |
| 6022 | `patches` | property | http://www.w3.org/ns/solid/terms#patches | The document to which this patch applies. |
| 6023 | `privateLabelIndex` | property | http://www.w3.org/ns/solid/terms#privateLabelIndex | Points to an unlisted label index resource. |
| 6024 | `privateTypeIndex` | property | http://www.w3.org/ns/solid/terms#privateTypeIndex | Points to an unlisted type index resource. |
| 6025 | `publicTypeIndex` | property | http://www.w3.org/ns/solid/terms#publicTypeIndex | Points to a listed type index resource. |
| 6026 | `read` | property | http://www.w3.org/ns/solid/terms#read | Indicates if a message has been read or not. This property should have a boolean datatype. |
| 6027 | `storageDescription` | property | http://www.w3.org/ns/solid/terms#storageDescription | Refers to the resource that provides a description of the storage containing this resource. |
| 6028 | `nonvolatileMemoryQuota` | property | http://www.w3.org/ns/solid/terms#storageQuota | The quota of non-volatile memory that is available for the account (in bytes) |
| 6029 | `nonvolatileMemoryUsage` | property | http://www.w3.org/ns/solid/terms#storageUsage | The amount of non-volatile memory that the account have used (in bytes) |
| 6030 | `timeline` | property | http://www.w3.org/ns/solid/terms#timeline | Timeline for a given resource. |
| 6031 | `typeIndex` | property | http://www.w3.org/ns/solid/terms#typeIndex | Points to a TypeIndex resource. |
| 6032 | `where` | property | http://www.w3.org/ns/solid/terms#where | The conditions the document and the inserted and deleted triple patterns need to satisfy in order for the patch to be applied. |

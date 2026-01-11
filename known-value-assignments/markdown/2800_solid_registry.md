# solid Known Values Registry

## Ontology Information

| Property | Value |
|----------|-------|
| **Name** | solid |
| **Source URL** | http://www.w3.org/ns/solid/terms# |
| **Start Code Point** | 2800 |
| **Processing Strategy** | StandardRDF |

## Statistics

| Metric | Value |
|--------|-------|
| **Total Entries** | 33 |
| **Code Point Range** | 2800 - 2832 |

## Entries

| Codepoint | Name | Type | URI | Description |
|-----------|------|------|-----|-------------|
| 2800 | `solid:Account` | class | http://www.w3.org/ns/solid/terms#Account | A Solid account. |
| 2801 | `solid:Inbox` | class | http://www.w3.org/ns/solid/terms#Inbox | A resource containing notifications. |
| 2802 | `solid:insertdeletePatch` | class | http://www.w3.org/ns/solid/terms#InsertDeletePatch | A class of patch expressing insertions, deletions, and conditional modifications to a resource that has an RDF-based representation. |
| 2803 | `solid:listedTypeIndex` | class | http://www.w3.org/ns/solid/terms#ListedDocument | Listed Type Index is a registry of resources that are publicly discoverable by outside users and applications. |
| 2804 | `solid:Notification` | class | http://www.w3.org/ns/solid/terms#Notification | A notification resource. |
| 2805 | `solid:Patch` | class | http://www.w3.org/ns/solid/terms#Patch | A patch expresses conditional modifications to a resource that has an RDF-based representation. |
| 2806 | `solid:Timeline` | class | http://www.w3.org/ns/solid/terms#Timeline | A resource containing time ordered items and sub-containers.  Sub-containers may be desirable in file based systems to split the timeline into logical components e.g. /yyyy-mm-dd/ as used in ISO 8061. |
| 2807 | `solid:typeIndex` | class | http://www.w3.org/ns/solid/terms#TypeIndex | A index of type registries for resources. Applications can register the RDF type they use and list them in the index resource. |
| 2808 | `solid:typeRegistration` | class | http://www.w3.org/ns/solid/terms#TypeRegistration | The registered types that map a RDF classes/types to their locations using either `instance` or `instanceContainer` property. |
| 2809 | `solid:unlistedTypeIndex` | class | http://www.w3.org/ns/solid/terms#UnlistedDocument | Unlisted Type Index is a registry of resources that are private to the user and their apps, for types that are not publicly discoverable. |
| 2810 | `solid:account` | property | http://www.w3.org/ns/solid/terms#account | A solid account belonging to an Agent. |
| 2811 | `solid:deletes` | property | http://www.w3.org/ns/solid/terms#deletes | The triple patterns this patch removes from the document. |
| 2812 | `solid:registryClass` | property | http://www.w3.org/ns/solid/terms#forClass | A class that is used to map an listed or unlisted type index. |
| 2813 | `solid:inboxDeprecated` | property | http://www.w3.org/ns/solid/terms#inbox | Deprecated pointer to a Linked Data Notifications inbox; please use http://www.w3.org/ns/ldp#inbox instead. |
| 2814 | `solid:inserts` | property | http://www.w3.org/ns/solid/terms#inserts | The triple patterns this patch adds to the document. |
| 2815 | `solid:instance` | property | http://www.w3.org/ns/solid/terms#instance | Maps a type to an individual resource, typically an index or a directory listing resource. |
| 2816 | `solid:instanceContainer` | property | http://www.w3.org/ns/solid/terms#instanceContainer | Maps a type to a container which the client would have to list to get the instances of that type. |
| 2817 | `solid:loginEndpoint` | property | http://www.w3.org/ns/solid/terms#loginEndpoint | The login URI of a given server. |
| 2818 | `solid:logoutEndpoint` | property | http://www.w3.org/ns/solid/terms#logoutEndpoint | The logout URI of a given server. |
| 2819 | `solid:notification` | property | http://www.w3.org/ns/solid/terms#notification | Notification resource for an inbox. |
| 2820 | `solid:oidcIssuer` | property | http://www.w3.org/ns/solid/terms#oidcIssuer | The preferred OpenID Connect issuer URI for a given WebID. |
| 2821 | `solid:owner` | property | http://www.w3.org/ns/solid/terms#owner | A person or social entity that is considered to have control, rights, and responsibilities over a data storage. |
| 2822 | `solid:patches` | property | http://www.w3.org/ns/solid/terms#patches | The document to which this patch applies. |
| 2823 | `solid:privateLabelIndex` | property | http://www.w3.org/ns/solid/terms#privateLabelIndex | Points to an unlisted label index resource. |
| 2824 | `solid:privateTypeIndex` | property | http://www.w3.org/ns/solid/terms#privateTypeIndex | Points to an unlisted type index resource. |
| 2825 | `solid:publicTypeIndex` | property | http://www.w3.org/ns/solid/terms#publicTypeIndex | Points to a listed type index resource. |
| 2826 | `solid:read` | property | http://www.w3.org/ns/solid/terms#read | Indicates if a message has been read or not. This property should have a boolean datatype. |
| 2827 | `solid:storageDescription` | property | http://www.w3.org/ns/solid/terms#storageDescription | Refers to the resource that provides a description of the storage containing this resource. |
| 2828 | `solid:nonvolatileMemoryQuota` | property | http://www.w3.org/ns/solid/terms#storageQuota | The quota of non-volatile memory that is available for the account (in bytes) |
| 2829 | `solid:nonvolatileMemoryUsage` | property | http://www.w3.org/ns/solid/terms#storageUsage | The amount of non-volatile memory that the account have used (in bytes) |
| 2830 | `solid:timeline` | property | http://www.w3.org/ns/solid/terms#timeline | Timeline for a given resource. |
| 2831 | `solid:typeIndex` | property | http://www.w3.org/ns/solid/terms#typeIndex | Points to a TypeIndex resource. |
| 2832 | `solid:where` | property | http://www.w3.org/ns/solid/terms#where | The conditions the document and the inserted and deleted triple patterns need to satisfy in order for the patch to be applied. |

# MongoDB Optimizations

- [Summary](#summary)
- [Optimzations](#optimzations)
- [Discovering Common Query Patterns and Crafting Tailored Indexes](#discovering-common-query-patterns-and-crafting-tailored-indexes)
- [Creating Your Indexes](#creating-your-indexes)
- [Analyzing Queries and Index Optimization](#analyzing-queries-and-index-optimization)
- [Insights from MongoDB Experts](#insights-from-mongodb-experts)

## Summary
I've been a MongoDB user for quite some time now, and I'm excited to share my experiences with you in this blog. Here, I'll delve into the optimizations that my colleagues and I have implemented to achieve a remarkable 10x improvement in query performance and efficiency.

After diligently applying these optimizations, the results were truly impressive. Query times saw a substantial reduction, and our meticulously crafted indexes performed flawlessly. This blog serves as a testament to the positive impact of our efforts, offering valuable insights into how you can supercharge your MongoDB queries and harness the full potential of this powerful database technology.

## Optimzations

### Discovering Common Query Patterns and Crafting Tailored Indexes

Enhancing the performance of your MongoDB queries is a fundamental and critical undertaking. A cornerstone of this journey involves the creation of indexes customized to suit the recurring query patterns your database encounters most frequently.

Unleashing the full potential of your MongoDB database begins with the identification of these repetitive query patterns, which lie at the core of your application's functionality. Once you've zeroed in on these pivotal operations, the development of well-crafted indexes that align with these patterns becomes a game-changing strategy.

This approach empowers MongoDB to swiftly pinpoint and retrieve the data you require, leading to a significant enhancement in query performance. Such optimization not only supercharges your application's responsiveness but also guarantees that MongoDB operates at peak efficiency, resulting in a seamless user experience and enabling your application to scale gracefully.

### Creating Your Indexes

#### Apply the ESR(Equality, Sort, Range) Rule for Effective Index Creation

* **Equality** fields: Begin your index with fields used in exact match queries, such as locating documents where a specific attribute, like "name," precisely matches a given value, such as "Hitesh."
* **Sort** fields: Follow the equality fields with those used for sorting query results. For example, if you're searching for documents where the "age" field exceeds 18, consider "age" as a sort field.
* **Range** fields: Conclude the index with fields needed to find documents within specific value ranges. For instance, if you're searching for documents where the "age" field falls between 20 and 30, designate "age" as a range field.

While the ESR rule provides valuable guidance for constructing compound indexes, remember it's not a rigid law. Consider these additional factors:

* Field order within the index significantly impacts its performance, with more selective equality fields enhancing index efficiency.
* Keep the index concise by minimizing the number of fields, as each additional field may potentially slow down query performance.
* Take into account field cardinality. High cardinality fields with numerous distinct values can influence index efficiency.

Here are some illustrative examples of compound indexes that align with the ESR rule:

* **`{ product_id: 1, customer_id: 1 }`**: Perfect for queries needing precise matches on the "product_id" field (e.g., searching for a specific product) and subsequent sorting by "customer_id" (perhaps to analyze customer purchase behavior).

* **`{ product_category: 1, price: 1 }`**: Tailored for queries requiring exact matches on the "product_category" field (e.g., all items in a specific category) and then sorting by "price" for comparison shopping or price range analysis.

* **`{ location: 1, delivery_date: 1 }`**: Designed for queries involving a geographic area or "location" (e.g., searching for products available in a specific region) and then sorting the results by "delivery_date" to prioritize shipping times.

For more details read [here](https://www.mongodb.com/docs/manual/tutorial/equality-sort-range-rule/).

#### Understanding Index Prefixes in MongoDB (Prefix Rule)

In MongoDB indexing, the prefix rule stipulates that an index can effectively support queries involving a subset of its fields, as long as this subset constitutes a prefix of the index key pattern. Specifically, a prefix, in the context of a compound index, comprises one or more keys located at the beginning of the index key pattern.

For instance, contemplate the following compound index:
```js
{ firstName: 1, age: 1 }
```

This index is capable of supporting queries like:
```js
db.users.find({ firstName: "Raj" })
db.users.find({ firstName: "Raj" }).sort({ age: 1 })
```

Remarkably, it can also facilitate a query like:
```js
db.users.find({ firstName: "Raj" }).sort({ age: 1 }).limit(10)
```
This is because the query exclusively engages the "firstName" and "age" fields, both of which constitute an index prefix.

The prefix rule proves particularly valuable for optimizing queries requiring result sorting. Imagine a scenario where you must pinpoint all records where the "firstName" matches "Raj" and subsequently arrange them by the "age" field. With the aforementioned index in place, this query can efficiently arrange results, sidestepping the need to scan the entire collection.

For further insights, refer to the official MongoDB documentation on [Index Prefixes](https://www.mongodb.com/docs/manual/core/indexes/index-types/index-compound/#index-prefixes).

#### Ensuring Your Indexes Fit Comfortably in RAM

In the MongoDB world, ensuring that your indexes reside comfortably in RAM is a mission-critical endeavor. MongoDB's indexing system is the backbone of rapid document retrieval, enabling the database to swiftly pinpoint and retrieve documents that match specific criteria. When these crucial indexes are readily available in RAM, it leads to significantly faster query execution compared to fetching data from disk.

Example:

Let's consider an example with a MongoDB collection called "products" for an e-commerce website. This collection contains information about various products, including their names, prices, categories, and customer reviews.


```json
{
  "_id": 1,
  "name": "Smartphone",
  "price": 599.99,
  "category": "Electronics",
  "reviews": [
    { "user": "User1", "rating": 5 },
    { "user": "User2", "rating": 4 },
    { "user": "User3", "rating": 4 }
  ]
}
```

Now, consider a query that retrieves all products in the "Electronics" category with a price below ₹700 and sorts them by price:

```js
db.products.find({ "category": "Electronics", "price": { $lt: 700 } }).sort({ "price": 1 })
```

To optimize this query, you create an index on the "category" and "price" fields:

```js
db.products.createIndex({ "category": 1, "price": 1 })
```

But how do you ensure this index, or any other index, fits snugly within your available RAM? MongoDB offers the **`collStats()`** method to help with this.

```js
const stats = db.products.stats();  // Collect statistics about the "products" collection
print("Index Sizes (Bytes):");
printjson(stats.indexSizes);

// Check if the index "category_1_price_1" fits in RAM
const indexSizeInBytes = stats.indexSizes["category_1_price_1"];
const ramSizeInBytes = stats.storageSize;
if (indexSizeInBytes <= ramSizeInBytes) {
  print("The index 'category_1_price_1' fits comfortably in RAM.");
} else {
  print("The index 'category_1_price_1' does not fit entirely in RAM. Consider optimizing memory resources.");
}
// Inside mongo shell
```

You can run this script inside the Mongo shell.

In this script:

* `stats.indexSizes` provides information about the sizes of your collection's indexes.
* `stats.storageSize` gives the storage size of the entire collection, including data and indexes.

By comparing the size of your specific index with the overall storage size, you can determine whether the index fits in RAM or if there's room for optimization.

Optimizing memory usage, especially for frequently queried indexes, can significantly improve query performance and ensure a responsive application. Regularly monitoring index sizes with `collStats()` helps you make informed decisions about index optimization and resource allocation.

For further insights, refer to the official MongoDB documentation on [Index Prefixes](https://www.mongodb.com/docs/manual/tutorial/ensure-indexes-fit-ram/).


### Analyzing Queries and Index Optimization

Consider engaging in this practice every two weeks or on a monthly basis. If your frequently executed queries are evolving, this routine will aid in enhancing the efficiency of your system.

#### Use indexStats to check indexes performance

**`indexStats`** in MongoDB is a feature that provides statistics about the performance of indexes on a particular collection. It allows you to monitor how well your indexes are serving your queries and can help you identify potential issues or optimization opportunities.

**Why IndexStats is Important?**

Indexes are critical for efficient query performance in MongoDB. By using indexes, MongoDB can quickly locate and retrieve documents that match query criteria. However, not all indexes are created equal, and their performance can vary based on factors such as size, usage, and fragmentation. This is where **`indexStats`** comes in handy. It provides insights into the effectiveness of your indexes, helping you make informed decisions about index maintenance or optimization.

```js
db.myCollection.aggregate([
  { $indexStats: {} }
]);
```
The result, sourced from MongoDB Documentation, appears as follows:
```js
{
   "name" : "item_1_quantity_1",
   "key" : { "item" : 1, "quantity" : 1 },
   "host" : "examplehost.local:27018",
   "accesses" : {
      "ops" : NumberLong(1),
      "since" : ISODate("2020-02-10T21:11:23.059Z")
   },
   "shard" : "shardA",      // Available starting in MongoDB 4.2.4 if run on sharded cluster
   "spec" : {               // Available starting in MongoDB 4.2.4
      "v" : 2,
      "key" : { "item" : 1, "quantity" : 1 },
      "name" : "item_1_quantity_1"
   }
}
{
   "name" : "item_1_price_1",
   "key" : { "item" : 1, "price" : 1 },
   "host" : "examplehost.local:27018",
   "accesses" : {
      "ops" : NumberLong(1),
      "since" : ISODate("2020-02-10T21:11:23.233Z")
   },
   "shard" : "shardA",      // Available starting in MongoDB 4.2.4 if run on sharded cluster
   "spec" : {               // Available starting in MongoDB 4.2.4
      "v" : 2,
      "key" : { "item" : 1, "price" : 1 },
      "name" : "item_1_price_1"
   }
}
{
   "name" : "item_1",
   "key" : { "item" : 1 },
   "host" : "examplehost.local:27018",
   "accesses" : {
      "ops" : NumberLong(0),
      "since" : ISODate("2020-02-10T21:11:22.947Z")
   },
   "shard" : "shardA",      // Available starting in MongoDB 4.2.4 if run on sharded cluster
   "spec" : {               // Available starting in MongoDB 4.2.4
      "v" : 2,
      "key" : { "item" : 1 },
      "name" : "item_1"
   }
}
{
   "name" : "_id_",
   "key" : { "_id" : 1 },
   "host" : "examplehost.local:27018",
   "accesses" : {
      "ops" : NumberLong(0),
      "since" : ISODate("2020-02-10T21:11:18.298Z")
   },
   "shard" : "shardA",      // Available starting in MongoDB 4.2.4 if run on sharded cluster
   "spec" : {               // Available starting in MongoDB 4.2.4
      "v" : 2,
      "key" : { "_id" : 1 },
      "name" : "_id_"
   }
}
```

##### Removing Inefficient Indexes Across Shards

Here's an example of removing inconsistent indexes across shards, adapted from MongoDB's official documentation:

```js
const pipeline = [
    // Get indexes and the shards that they belong to.
    {$indexStats: {}},
    // Attach a list of all shards which reported indexes to each document from $indexStats.
    {$group: {_id: null, indexDoc: {$push: "$$ROOT"}, allShards: {$addToSet: "$shard"}}},
    // Unwind the generated array back into an array of index documents.
    {$unwind: "$indexDoc"},
    // Group by index name.
    {
        $group: {
            "_id": "$indexDoc.name",
            "shards": {$push: "$indexDoc.shard"},
            // Convert each index specification into an array of its properties
            // that can be compared using set operators.
            "specs": {$push: {$objectToArray: {$ifNull: ["$indexDoc.spec", {}]}}},
            "allShards": {$first: "$allShards"}
        }
    },
    // Compute which indexes are not present on all targeted shards and
    // which index specification properties aren't the same across all shards.
    {
        $project: {
            missingFromShards: {$setDifference: ["$allShards", "$shards"]},
            inconsistentProperties: {
                 $setDifference: [
                     {$reduce: {
                         input: "$specs",
                         initialValue: {$arrayElemAt: ["$specs", 0]},
                         in: {$setUnion: ["$$value", "$$this"]}}},
                     {$reduce: {
                         input: "$specs",
                         initialValue: {$arrayElemAt: ["$specs", 0]},
                         in: {$setIntersection: ["$$value", "$$this"]}}}
                 ]
             }
        }
    },
    // Only return output that indicates an index was inconsistent, i.e. either a shard was missing
    // an index or a property on at least one shard was not the same on all others.
    {
        $match: {
            $expr:
                {$or: [
                    {$gt: [{$size: "$missingFromShards"}, 0]},
                    {$gt: [{$size: "$inconsistentProperties"}, 0]},
                ]
            }
        }
    },
    // Output relevant fields.
    {$project: {_id: 0, indexName: "$$ROOT._id", inconsistentProperties: 1, missingFromShards: 1}}
];
```

Run the aggregration Pipeline

```js
db.getSiblingDB("test").reviews.aggregate(pipeline)
```

When you run this aggregation pipeline, it will identify indexes that are either missing on certain shards or have inconsistent properties across shards. The result will show the index names, properties that are inconsistent, and which shards the indexes are missing from. This information can be valuable for cleaning up and optimizing your indexes in a sharded MongoDB environment.

For example:
```js
{ "missingFromShards" : [ "shardB" ], "inconsistentProperties" : [ ], "indexName" : "page_1_score_1" }
{ "missingFromShards" : [ ], "inconsistentProperties" : [ { "k" : "expireAfterSeconds", "v" : 60 }, { "k" : "expireAfterSeconds", "v" : 600 } ], "indexName" : "reviewDt_1" }
```

References: [IndexStats](https://www.mongodb.com/docs/manual/reference/operator/aggregation/indexStats/),
[Inconsistent Indexes](https://www.mongodb.com/docs/manual/tutorial/manage-indexes/#find-inconsistent-indexes-across-shards),
[Stats](https://www.mongodb.com/docs/manual/reference/method/db.collection.stats/),
[Stats 2](https://www.mongodb.com/docs/manual/reference/method/db.stats/)

#### Analyse your queries with keyhole

* Begin by installing and configuring the Keyhole tool on the desired machine for MongoDB log analysis. Keyhole can be obtained from its official website, where you will find installation instructions tailored to your specific operating system.
* Commence the Keyhole tool with the appropriate settings. Keyhole offers the flexibility to specify the location of your MongoDB log file and various options for fine-tuning log analysis. Below is an illustrative command to initiate Keyhole and scrutinize MongoDB logs:

```bash
keyhole --log-file /var/log/mongodb/mongod.log
```
Make sure to replace `/var/log/mongodb/mongod.log` with the actual path to your MongoDB log file.

* For the generation of an HTML Summary Report, consider utilizing the simagix/maobi Docker image.

To delve deeper into Keyhole and its usage, refer to the [offical documentation](https://www.mongodb.com/blog/post/peek-at-your-mongodb-clusters-like-a-pro-with-keyhole-part-1)

**Please Note**: When employing a MongoDB Atlas Cluster, you gain access to a built-in dashboard that facilitates query profiling and debugging within the cluster. However, it retains only a limited dataset. If your objective is to analyze MongoDB logs on a weekly or monthly basis, the **Keyhole** tool proves invaluable in this context.


#### Leveraging the Explain Method for Query Optimization

The MongoDB **`explain()`** method serves as a valuable resource for gaining insights into how MongoDB intends to execute a given query, ultimately aiding in query performance optimization.

To employ the **`explain()`** method, you simply provide the query you wish to dissect as an argument to the method. For instance, the following command elucidates a query that seeks all documents in the `myCollection` collection with the `name` field set to "Hitesh Joshi":

```js
db.myCollection.explain({ name: "Hitesh Joshi" });
```

The output from the **explain()** method furnishes a document containing essential information, notably:

* **`queryPlanner`**: This section of the output unveils MongoDB's planned strategy for executing the query.

* **`executionStats`**: In this section, you'll find statistics pertaining to the query's execution, including the count of documents scanned and the query's execution duration.

```js
{
  "queryPlanner": {
    "plannerVersion": 1,
    "namespace": "myDatabase.myCollection",
    "indexFilterSet": [
      {
        "filter": {
          "name": "Hitesh Joshi"
        },
        "index": "name_1"
      }
    ],
    "winningPlan": {
      "stage": "IXSCAN",
      "keyPattern": {
        "name": 1
      },
      "indexName": "name_1",
      "direction": "forward",
      "filter": {
        "name": "Hitesh Joshi"
      }
    }
  },
  "executionStats": {
    "totalDocsExamined": 100,
    "totalDocsMatched": 1,
    "totalTimeMillis": 10,
    "executionTimeMillis": 5,
    "scanAndOrderStagesTimeMillis": 5
  }
}
```

In this illustration, the winning plan involves an **IXSCAN** stage, indicating that MongoDB will utilize the name_1 index to execute the query. Notably, the totalDocsExamined field reveals that MongoDB scanned 100 documents during query execution, while the **totalTimeMillis** field signifies a query execution time of 10 milliseconds.

Leveraging the insights gained from the explain() output, you can take informed steps to optimize query performance. For instance, if you observe a high number of document scans, creating an index on the queried field can be a prudent action. Additionally, the explain() output can help you pinpoint and resolve potential query-related issues.

Sometimes you will also encounter **rejectedPlans** also.
```js
{
  "queryPlanner": {
    "plannerVersion": 1,
    "namespace": "myDatabase.myCollection",
    "winningPlan": {
      // Details of the winning plan
    },
    "rejectedPlans": [
      {
        // Details of the first rejected plan
      },
      {
        // Details of the second rejected plan
      }
    ]
  },
}
```
Typically, **MongoDB** includes `rejectedPlans` when there are multiple query plans to choose from, and it's helpful to understand why certain plans were not selected. Each rejected plan will have its own set of details, similar to the winning plan, providing insight into why it was not chosen.

If you don't see the `rejectedPlans` field in the explain() output, it means that MongoDB's query planner did not consider or reject alternative plans, and it proceeded with the winning plan directly. The presence of rejectedPlans is most common in complex queries where multiple index choices and strategies are available.

While reducing the number of rejected plans is generally beneficial, it's important to strike a balance between query planning time and query execution efficiency. The ultimate goal is to choose the most efficient plan for each query while minimizing unnecessary planning overhead.

Note: 
* **IXSCAN** stands for Index Scan. It uses an index to find the documents that match the query criteria. This is a more efficient way to execute queries when there is an index on the field that you are querying.

* **COLLSCAN** denotes "Collection Scan," involving a full collection scan to identify matching documents. While less efficient, it becomes necessary when no index exists for the queried field. Minimizing `COLLSCAN` is pivotal for optimizing query speed, as collection scans tend to be slower.


### Insights from MongoDB Experts

Please note that the effectiveness of these optimizations can vary depending on your specific database queries and structure. These recommendations are based on expert advice and have proven beneficial for our organization's database structure, enhancing query performance.

#### Document Size

Optimal document size typically falls within the range of 1-2 MB. This size range places less strain on the MongoDB server and allows various operations within the aggregation pipeline to execute smoothly.

#### Indexing Considerations

While the ideal number of indexes may vary based on your hardware and database size, a general guideline is to create 15-20 indexes. This recommendation stems from the expertise of MongoDB professionals, emphasizing the advantages of having a sufficient number of indexes. This approach helps ensure that a significant portion of your data can be efficiently stored within indexes, ultimately resulting in faster query performance.


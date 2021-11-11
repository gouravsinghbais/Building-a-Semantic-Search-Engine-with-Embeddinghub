# Building-a-Semantic-Search-Engine-with-Embeddinghub

Embeddinghub is a database built for machine learning embeddings. It is built with four goals in mind.

* Store embeddings durably and with high availability
* Allow for approximate nearest neighbor operations
* Enable other operations like partitioning, sub-indices, and averaging
* Manage versioning, access control, and rollbacks painlessly

Prior to Embeddinghub, many organizations would use four different tools to achieve these four goals. With Embeddinghub, you get a database that’s built from the ground up to achieve this functionality.

## Step 1: Installation 

EmbeddingHub can be downloaded using python package manager PIP. 
```
!pip install embeddinghub
```
Without a server, the Embeddinghub client can be utilised. When using embeddings in a research context where a database server is not required, this is advantageous. If that is indeed the case, go ahead and move on to the next step. 
Otherwise, You can run Embeddinghub locally and map the container's main port to your host's port using this docker command. 
```
docker run featureformcom/embeddinghub -p 7462:7462
```
Once the installation is done, to use the EmbeddingHub database in your code you would have to create a python client that would interact with the database to perform the database operations like read, write, delete etc. 

## Step 2: Initialize Python Client

A local client can be initialised like this:
```
import embeddinghub as eh
hub = eh.connect(eh.LocalConfig("data/"))
```
Here connect initialises the connection with the database and LocalConfig tells the client that connection would be made locally. You can specify any client name you want to connect to using the following line:
```
hub = eh.connect(eh.Config())
```

## Step 3: Creating a Space 

Once the client is initialised you need to define a space, embedding data is written and read from the spaces. A space is like a table in a relational database where you would be storing the data. 
```
## create a space named demo with the dimension of your data
space = hub.create_space("demo", dims=768)
```

## Step 4: Use Database

After space is created, the database is now ready to write and read the data. To store the data in the database **"set"** function is used that takes a dictionary containing sentences as keys and embeddings as values. To write a single key, value pair **"set"** function can be used while for writing data in bulk **"multiset"** function is used. 
```
## write data in database
space.multiset(embeddings)
```

Storing the data is not enough you need to retrieve it when needed and perform the necessary operations. To read the data from the database you can create a new client but this time you need to get the space that you have already created. 
```
## get space where data is stored
space = hub.get_space("demo")
```

Once you are connected to space you can query the data stored in that space. To get specific sentence embeddings you can use the **"get"** function while to read multiple embeddings at a time you would have to use the **"multiget"** function. 
```
## retrieve multiple embeddings at a time
embed = space.multiget(embeddings.keys())
getEmbeddings = dict(zip(embeddings.keys(), embed))
```
There is one more functionality that you should be aware of is **"delete"**. You can delete a space or multiple spaces at a time. 
```
## delete single space 
spcae.delete("a")
## delete multiple spaces
space.multidelete(["a", "b", "c"])
```

# References  
- [Semantic Search Engine with Sentence BERT](https://evergreenllc2020.medium.com/semantic-search-engine-with-s-abbfb3cd9377)
- [EmbeddingHub Database](https://docs.featureform.com/)

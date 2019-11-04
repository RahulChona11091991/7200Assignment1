# ------------- Installing Library -------------
install.packages("extrafont")
install.packages("igraph")
install.packages("CINNA")
install.packages("devtools")
if (!require("ForceAtlas2")) devtools::install_github("analyxcompany/ForceAtlas2")


# ------------- Importing Library -------------
library(extrafont) # Optional
library(readr)
library(igraph)
library(CINNA)
library("ForceAtlas2")


# ------------- Reading nodes from file -------------
nodes <- read.delim("/Users/xbox/PycharmProjects/7200Assignment/data/allPosts.tsv")


# ------------- Reading links from file -------------
links <- read.delim("/Users/xbox/PycharmProjects/7200Assignment/data/askerAnswerer.tsv")


# ------------- Understanding Data -------------
head(nodes)
head(links)

#-------------------------------------------------------------------------------------
#--------------------------------With Loops-------------------------------------------
#-------------------------------------------------------------------------------------

#net <- graph.data.frame(links[,-1], directed=T)
net <- graph.data.frame(links, unique(nodes$user_id), directed=T)

# ------------- Finding degree of all nodes in Complete Graph -------------
deg <- degree(net, mode="all")
V(net)$size <- deg*3

# ------------- Printing all Components of Complete Graph -------------
graph_extract_components(net)

# ------------- Extracting Giant Component From Complete Graph -------------
giant_component_sub_graph <- giant_component_extract(net)
print(giant_component_sub_graph)

# ------------- Writing Giant Component To File -------------
write_graph(giant_component_sub_graph[[1]], file = "/Users/xbox/PycharmProjects/7200Assignment/data/asker-answerer-giant.tsv", format = c("ncol"))

# ------------- Graph Plot With Loops -------------
#Method 1
par(mar=c(0,0,0,0))
plot(net, vertex.size=2, vertex.color = rainbow(10, .8, .8, alpha= .8), vertex.label.color = "black", vertex.label.cex = 0.4, edge.arrow.size = 0.3, edge.arrow.width = 0.4, edge.color = "gray", vertex.label=NA)

#Method 2
par(mfrow=c(2,2), mar=c(1,1,1,1))
plot(net, layout=layout.random, main="random", vertex.size=2, edge.width=1,edge.arrow.size=0.02, vertex.label=NA)

#Method 3 - Time Consuming Process
layout <- layout.forceatlas2(net, iterations=2000, directed = TRUE, plotstep=0, plotlabels = FALSE)

# ------------- Plot Giant Component -------------
plot(giant_component_sub_graph[[1]], main="Giant Component", vertex.size=8, vertex.color = rainbow(10, .8, .8, alpha= .8), vertex.label.color = "black", vertex.label.cex = 0.4, vertex.label.degree = -pi/2, edge.arrow.size = 0.3, edge.arrow.width = 0.4, edge.color = "gray")

# ------------- Plotting Components Complete Graph - With Loops  -------------
plot(net,layout=layout_components(net), main="Plotting Component With Loops", vertex.size=2, vertex.color = rainbow(10, .8, .8, alpha= .8), vertex.label.color = "black", vertex.label.cex = 0.4, vertex.label.degree = -pi/2, edge.arrow.size = 0.3, edge.arrow.width = 0.4, edge.color = "gray")

# ------------- Plotting Giant Components - With Loops  -------------
plot(net,layout=layout_components(giant_component_sub_graph[[1]]), main="Plotting Giant Component With Loops",vertex.size=4, vertex.label=NA)




#-------------------------------------------------------------------------------------
#-----------------------------Without Loops-------------------------------------------
#-------------------------------------------------------------------------------------

#net_without_loops - if a user has answered its own question then skipping that edge.
net_without_loops <-simplify(net,remove.multiple =F, remove.loops =T)
E(net_without_loops)
V(net_without_loops)
graph_extract_components(net_without_loops)

# ------------- Extracting Giant Component From Complete Graph Without loops -------------
giant_component_sub_graph_without_Loops <- giant_component_extract(net_without_loops)
print(giant_component_sub_graph_without_Loops)

# ------------- Graph Plot Without Loops -------------
par(mar=c(0,0,0,0))
plot(net_without_loops, main="Complete Graph Without Loops",vertex.size=2, vertex.color = rainbow(10, .8, .8, alpha= .8), vertex.label.color = "black", vertex.label.cex = 0.4, edge.arrow.size = 0.3, edge.arrow.width = 0.4, edge.color = "gray", vertex.label=NA)

# ------------- Plot Giant Component Without Loops -------------
plot(giant_component_sub_graph_without_Loops[[1]], main="Giant Component", vertex.size=8, vertex.color = rainbow(10, .8, .8, alpha= .8), vertex.label.color = "black", vertex.label.cex = 0.4, vertex.label.degree = -pi/2, edge.arrow.size = 0.3, edge.arrow.width = 0.4, edge.color = "gray")

# ------------- Plotting all Component Without Loops  -------------
plot(net_without_loops,layout=layout_components(net_without_loops), main="Plotting all Component Without Loops", vertex.size=2, vertex.color = rainbow(10, .8, .8, alpha= .8), vertex.label.color = "black", vertex.label.cex = 0.4, vertex.label.degree = -pi/2, edge.arrow.size = 0.3, edge.arrow.width = 0.4, edge.color = "gray", vertex.label=NA)




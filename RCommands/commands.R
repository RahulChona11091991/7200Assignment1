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
library(data.table)

# ------------- Reading nodes from file -------------
nodes <- fread("./data/allPosts.tsv",skip=1, select = c(1:2), fill = TRUE)


# ------------- Reading links from files -------------
linksARN <- fread("./data/1-ARN.tsv",skip=1, select = c(1:2), fill = TRUE)
linksABAN <- fread("./data/2-ABAN.tsv",skip=1, select = c(1:2), fill = TRUE)
linksCBEN <- fread("./data/3-CBEN.tsv",skip=1, select = c(1:2), fill = TRUE)
linksVBEN <- fread("./data/4-VBEN.tsv",skip=1, select = c(1:3), fill = TRUE)
linksVBEN2 <- fread("./data/5-VBEN2.tsv",skip=1, select = c(1:3), fill = TRUE)

# ------------- Understanding Data -------------
head(nodes)
head(linksARN)
head(linksABAN)
head(linksCBEN)
head(linksVBEN)
head(linksVBEN2)

#-------------------------------------------------------------------------------------
#-------------------------------- With Loops -------------------------------------------
#-------------------------------------------------------------------------------------

netARN <- graph.data.frame(linksARN, unique(nodes$user_id), directed=T)
netABAN <- graph.data.frame(linksABAN, unique(nodes$user_id), directed=T)
netCBEN <- graph.data.frame(linksCBEN, unique(nodes$user_id), directed=T)
netVBEN <- graph.data.frame(linksVBEN, unique(nodes$user_id), directed=T)
netVBEN2 <- graph.data.frame(linksVBEN2, unique(nodes$user_id), directed=T)

# ------------- Graph Plot With Loops -------------
#Method 1
par(mar=c(0,0,0,0))
plot(netARN, vertex.size=2, vertex.color = rainbow(10, .8, .8, alpha= .8), vertex.label.color = "black", vertex.label.cex = 0.4, edge.arrow.size = 0.3, edge.arrow.width = 0.4, edge.color = "gray", vertex.label=NA)
plot(netABAN, vertex.size=2, vertex.color = rainbow(10, .8, .8, alpha= .8), vertex.label.color = "black", vertex.label.cex = 0.4, edge.arrow.size = 0.3, edge.arrow.width = 0.4, edge.color = "gray", vertex.label=NA)
plot(netCBEN, vertex.size=2, vertex.color = rainbow(10, .8, .8, alpha= .8), vertex.label.color = "black", vertex.label.cex = 0.4, edge.arrow.size = 0.3, edge.arrow.width = 0.4, edge.color = "gray", vertex.label=NA)
plot(netVBEN, vertex.size=2, vertex.color = rainbow(10, .8, .8, alpha= .8), vertex.label.color = "black", vertex.label.cex = 0.4, edge.arrow.size = 0.3, edge.arrow.width = 0.4, edge.color = "gray", vertex.label=NA)
plot(netVBEN2, vertex.size=2, vertex.color = rainbow(10, .8, .8, alpha= .8), vertex.label.color = "black", vertex.label.cex = 0.4, edge.arrow.size = 0.3, edge.arrow.width = 0.4, edge.color = "gray", vertex.label=NA)

# Generate PDF Files
pdf(file="./Results/1-ARN.pdf")
plot(netARN, vertex.size=2, vertex.color = rainbow(10, .8, .8, alpha= .8), vertex.label.color = "black", vertex.label.cex = 0.4, edge.arrow.size = 0.3, edge.arrow.width = 0.4, edge.color = "gray", vertex.label=NA)
dev.off()

pdf(file="./Results/2-ABAN.pdf")
plot(netABAN, vertex.size=2, vertex.color = rainbow(10, .8, .8, alpha= .8), vertex.label.color = "black", vertex.label.cex = 0.4, edge.arrow.size = 0.3, edge.arrow.width = 0.4, edge.color = "gray", vertex.label=NA)
dev.off()

pdf(file="./Results/3-CBEN.pdf")
plot(netCBEN, vertex.size=2, vertex.color = rainbow(10, .8, .8, alpha= .8), vertex.label.color = "black", vertex.label.cex = 0.4, edge.arrow.size = 0.3, edge.arrow.width = 0.4, edge.color = "gray", vertex.label=NA)
dev.off()

pdf(file="./Results/4-VBEN.pdf")
plot(netVBEN, vertex.size=2, vertex.color = rainbow(10, .8, .8, alpha= .8), vertex.label.color = "black", vertex.label.cex = 0.4, edge.arrow.size = 0.3, edge.arrow.width = 0.4, edge.color = "gray", vertex.label=NA)
dev.off()

pdf(file="./Results/5-VBEN2.pdf")
plot(netVBEN2, vertex.size=2, vertex.color = rainbow(10, .8, .8, alpha= .8), vertex.label.color = "black", vertex.label.cex = 0.4, edge.arrow.size = 0.3, edge.arrow.width = 0.4, edge.color = "gray", vertex.label=NA)
dev.off()


# Generate PNG Files
jpeg(file="./Results/1-ARN.jpg", width = 480*4, height = 480*4)
plot(netARN, vertex.size=2, vertex.color = rainbow(10, .8, .8, alpha= .8), vertex.label.color = "black", vertex.label.cex = 0.4, edge.arrow.size = 0.3, edge.arrow.width = 0.4, edge.color = "gray", vertex.label=NA)
dev.off()

jpeg(file="./Results/2-ABAN.jpg", width = 480*4, height = 480*4)
plot(netABAN, vertex.size=2, vertex.color = rainbow(10, .8, .8, alpha= .8), vertex.label.color = "black", vertex.label.cex = 0.4, edge.arrow.size = 0.3, edge.arrow.width = 0.4, edge.color = "gray", vertex.label=NA)
dev.off()

jpeg(file="./Results/3-CBEN.jpg", width = 480*4, height = 480*4)
plot(netCBEN, vertex.size=2, vertex.color = rainbow(10, .8, .8, alpha= .8), vertex.label.color = "black", vertex.label.cex = 0.4, edge.arrow.size = 0.3, edge.arrow.width = 0.4, edge.color = "gray", vertex.label=NA)
dev.off()

jpeg(file="./Results/4-VBEN.jpg", width = 480*4, height = 480*4)
plot(netVBEN, vertex.size=2, vertex.color = rainbow(10, .8, .8, alpha= .8), vertex.label.color = "black", vertex.label.cex = 0.4, edge.arrow.size = 0.3, edge.arrow.width = 0.4, edge.color = "gray", vertex.label=NA)
dev.off()

jpeg(file="./Results/5-VBEN2.jpg", width = 480*4, height = 480*4)
plot(netVBEN2, vertex.size=2, vertex.color = rainbow(10, .8, .8, alpha= .8), vertex.label.color = "black", vertex.label.cex = 0.4, edge.arrow.size = 0.3, edge.arrow.width = 0.4, edge.color = "gray", vertex.label=NA)
dev.off()


#-------------------------------------------------------------------------------------
#-----------------------------Without Loops-------------------------------------------
#-------------------------------------------------------------------------------------


#net_without_loops - if a user has answered its own question then skipping that edge.
netARN_without_loops <-simplify(netARN,remove.multiple =F, remove.loops =T)
netABAN_without_loops <-simplify(netABAN,remove.multiple =F, remove.loops =T)
netCBEN_without_loops <-simplify(netCBEN,remove.multiple =F, remove.loops =T)
netVBEN_without_loops <-simplify(netVBEN,remove.multiple =F, remove.loops =T)
netVBEN2_without_loops <-simplify(netVBEN2,remove.multiple =F, remove.loops =T)

# ------------- Graph Plot Without Loops -------------
par(mar=c(0,0,0,0))
plot(netARN_without_loops, vertex.size=2, vertex.color = rainbow(10, .8, .8, alpha= .8), vertex.label.color = "black", vertex.label.cex = 0.4, edge.arrow.size = 0.3, edge.arrow.width = 0.4, edge.color = "gray", vertex.label=NA)
plot(netABAN_without_loops, vertex.size=2, vertex.color = rainbow(10, .8, .8, alpha= .8), vertex.label.color = "black", vertex.label.cex = 0.4, edge.arrow.size = 0.3, edge.arrow.width = 0.4, edge.color = "gray", vertex.label=NA)
plot(netCBEN_without_loops, vertex.size=2, vertex.color = rainbow(10, .8, .8, alpha= .8), vertex.label.color = "black", vertex.label.cex = 0.4, edge.arrow.size = 0.3, edge.arrow.width = 0.4, edge.color = "gray", vertex.label=NA)
plot(netVBEN_without_loops, vertex.size=2, vertex.color = rainbow(10, .8, .8, alpha= .8), vertex.label.color = "black", vertex.label.cex = 0.4, edge.arrow.size = 0.3, edge.arrow.width = 0.4, edge.color = "gray", vertex.label=NA)
plot(netVBEN2_without_loops, vertex.size=2, vertex.color = rainbow(10, .8, .8, alpha= .8), vertex.label.color = "black", vertex.label.cex = 0.4, edge.arrow.size = 0.3, edge.arrow.width = 0.4, edge.color = "gray", vertex.label=NA)


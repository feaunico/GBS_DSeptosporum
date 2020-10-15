library(gdsfmt)
library(SNPRelate)

snpgdsVCF2GDS("Dothi_1491.vcf", "D1491.gds", method="biallelic.only")

genofile <- snpgdsOpen("D1491.gds")


# no prunning : 
pca <- snpgdsPCA(genofile, num.thread=2,autosome.only = FALSE)




pc.percent <- pca$varprop*100
head(round(pc.percent, 2))

tab <- data.frame(sample.id = pca$sample.id,
    EV1 = pca$eigenvect[,1],    # the first eigenvector
    EV2 = pca$eigenvect[,2],    # the second eigenvector
    EV3 = pca$eigenvect[,2],    # the third eigenvector
    stringsAsFactors = FALSE)

write.table(tab, "Dothi_PCA_vectors.xls")
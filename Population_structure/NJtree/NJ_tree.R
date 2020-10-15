library(poppr)
library(ape)

library(vcfR)

Dothi.VCF <- read.vcfR("Dothi_1491.vcf")

gl.dothi <- vcfR2genlight(Dothi.VCF)
ploidy(gl.dothi) <- 1
tree <- aboot(gl.dothi, tree = "nj", distance = bitwise.dist, sample = 1000, showtree = F, cutoff = 50, quiet = T)
write.tree(tree, file = "Dothi_NJ_1000.tree", append = FALSE,
           digits = 10, tree.names = FALSE)
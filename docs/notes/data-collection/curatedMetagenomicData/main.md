# Download
## Metadata
```R
library(curatedMetagenomicData)
rowdata <- curatedMetagenomicData(
	"MetaCardis_2020_a.relative_abundance",
	dryrun = FALSE,
	rownames = "short"
)
data <- colData(rowdata[[1]])
dim(data)
write.csv(data, "metadata.csv", row.names = TRUE)
```                                       

## Feature Metadata
```R
rowdata <- rowData(data_gene[[1]])
data <- as.data.frame(feature_info)
write.csv(data, "feature_metadata.csv", row.names = TRUE)

```

## Feature-Sample Matrix
```R
assayNames(se_object)

data <- assays(se_object)[["relative_abundance"]]
write.csv(data, "gene_families.csv", row.names=TRUE)
```
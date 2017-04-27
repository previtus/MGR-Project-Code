import DatasetHandler.CreateDataset as CreateDataset

# Test functions to handle models

def DatasetTester(dataset, dataset_uid):
    # Load dataset, report input sizes


    # Cook features for various models

    # Report feature output sizes

    # Try top models - regular with fixed size or the "heatmap"


    return []


def main():
    [dataset, uniqueId] = CreateDataset.load_1200x_marked_299x299(desired_number=50, seed=42)
    DatasetTester(dataset, dataset_uid=uniqueId)

main()

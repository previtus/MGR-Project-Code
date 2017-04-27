import DatasetHandler.CreateDataset as CreateDataset
import ModelHandler.CreateModel.models as Models

# Test functions to handle models

def DatasetTester(dataset, dataset_uid):
    # Load dataset, report input sizes
    print "### Dataset reporting"
    print "w*h*ch:", dataset.img_width, "x", dataset.img_height, "x 3"

    # Cook features for various models
    all_models = Models.all_models()

    # Report feature output sizes

    # Try top models - regular with fixed size or the "heatmap"


    return []


def main():
    [dataset, uniqueId] = CreateDataset.load_1200x_marked_299x299(desired_number=50, seed=42)
    DatasetTester(dataset, dataset_uid=uniqueId)

main()

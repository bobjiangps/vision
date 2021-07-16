from models.pred import *

if __name__ == "__main__":
    model = init_model()
    results, labels = predict_label(model)
    print(labels)
    print(results)

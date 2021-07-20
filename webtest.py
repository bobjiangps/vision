from models.pred import *

if __name__ == "__main__":
    model = init_model()
    results, labels = predict(model)
    print(labels)
    print(results)

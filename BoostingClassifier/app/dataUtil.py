import logging

logger = logging.Logger('catch_all')


def base64ToCSV_DataFrame(base64String):
    import base64 as b64
    import pandas as pd
    from io import StringIO

    try:
        csv = b64.b64decode(base64String).decode('utf-8')
        dataframe = pd.read_csv(StringIO(csv))

        return dataframe

    except Exception as e:
        logger.error(e, exc_info=True)
        return str(e)


def dataprep(X):
    from sklearn.preprocessing import LabelEncoder

    try:

        for columName in X:
            if isinstance(X[columName][0], str):
                data = X[columName].tolist()
                labels_encoder = LabelEncoder()
                integers_encoded = labels_encoder.fit_transform(data)
                X[columName] = integers_encoded

        return X

    except Exception as e:
        logger.error(e, exc_info=True)
        return str(e)


def confusionMatrixGenerator(model, X_valid, y_valid):
    import base64
    from sklearn.metrics import plot_confusion_matrix
    import matplotlib.pyplot as plt
    try:
        plot_confusion_matrix(model, X_valid, y_valid)
        plt.savefig('save_as_a_png.png')

        with open("save_as_a_png.png", "rb") as img_file:
            encoded_string = base64.b64encode(img_file.read())

        return encoded_string.decode('utf-8')

    except Exception as e:
        logger.error(e, exc_info=True)
        return str(e)


def classificationReportGenerator(y_test, yhat):
    from sklearn.metrics import classification_report
    import pandas as pd

    try:
        report = (classification_report(y_test, yhat, output_dict=True))
        reportFrame = pd.DataFrame(report).transpose()
        indexList = reportFrame.index.tolist()
        reportFrame["Title"] = indexList
        reportFrame = reportFrame[['Title', 'precision', 'recall', 'f1-score', 'support']]
        reportFrame = reportFrame.drop("accuracy")

        return reportFrame

    except Exception as e:
        logger.error(e, exc_info=True)
        return str(e)
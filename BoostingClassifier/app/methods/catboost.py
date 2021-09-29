import logging

logger = logging.Logger('catch_all')


def boost(data, Parameters):
    try:
        import json
        from sklearn.metrics import accuracy_score
        from sklearn.preprocessing import LabelEncoder
        from app.dataUtil import base64ToCSV_DataFrame, dataprep, classificationReportGenerator, \
            confusionMatrixGenerator
        import numpy as np
        import pandas as pd
        from sklearn.model_selection import train_test_split
        import matplotlib.pylab as plt
        from sklearn.ensemble import GradientBoostingClassifier
        model = GradientBoostingClassifier()
        dependentParameter = Parameters.get('dependentParameter')
        independentParameter = Parameters.get('independentParameter')
        test_size = float(Parameters.get('test_size'))
        df = base64ToCSV_DataFrame(data)
        df_train = df
        # var_columns = [c for c in df_train.columns if c not in ['Outcome']]

        X = df_train.loc[:, independentParameter]
        y = df_train.loc[:, dependentParameter]
        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(y)

        X = dataprep(X)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
        model.fit(X_train, y_train)
        ypred = model.predict(X_test)
        y_test = label_encoder.inverse_transform(y_test)
        ypred = label_encoder.inverse_transform(ypred)

        reportFrame = classificationReportGenerator(y_test, ypred)

        encodedstr = confusionMatrixGenerator(model, X_test, y_test)

        acc = accuracy_score(y_test, ypred)
        acc = round(acc * 100, 2)
        print('Accuracy: %f' % acc)

        response = dict()
        response['Accuracy'] = acc
        response['report'] = json.loads(reportFrame.to_json(orient='records'))
        response['encodedstr'] = encodedstr
        print('Successful')
        return 1, str(json.dumps(response))


    except Exception as e:
        logger.error(e, exc_info=True)
        return 0, str(e)
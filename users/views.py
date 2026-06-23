# from django.shortcuts import render
# import numpy as np
# import pandas as pd
# from sklearn.svm import SVC
# from sklearn.preprocessing import StandardScaler
# from sklearn.model_selection import train_test_split
# from lime.lime_tabular import LimeTabularExplainer
# import matplotlib.pyplot as plt
# import os
# from django.conf import settings
# from django.conf.urls.static import static

# def train_models():
#     # Load Dataset (use your actual dataset path)
#     data = pd.read_csv('dataset.csv')

#     # Select Features and Targets
#     features = ['pos_0', 'pos_1', 'pos_noise_0', 'pos_noise_1',
#                 'spd_0', 'spd_1', 'spd_noise_0', 'spd_noise_1',
#                 'acl_0', 'acl_1', 'acl_noise_0', 'acl_noise_1',
#                 'hed_0', 'hed_1', 'hed_noise_0', 'hed_noise_1']
#     X = data[features]

#     # Binary Classification Target: Attack Detection (0 = Benign, 1 = Attack)
#     y_binary = data['attack']

#     # Multiclass Classification Target: Attack Type Detection
#     y_multiclass = data['attack_type']

#     # Train-Test Split
#     X_train, X_test, y_train_binary, y_test_binary = train_test_split(
#         X, y_binary, test_size=0.3, random_state=42
#     )
#     _, _, y_train_multiclass, y_test_multiclass = train_test_split(
#         X, y_multiclass, test_size=0.3, random_state=42
#     )

#     # Normalize Features
#     scaler = StandardScaler()
#     X_train = scaler.fit_transform(X_train)
#     X_test = scaler.transform(X_test)

#     # Train SVM Model for Binary Classification
#     svm_model_binary = SVC(probability=True, kernel='rbf', C=1)
#     svm_model_binary.fit(X_train, y_train_binary)

#     # Train SVM Model for Multiclass Classification
#     svm_model_multiclass = SVC(probability=True, kernel='rbf', C=1)
#     svm_model_multiclass.fit(X_train, y_train_multiclass)

#     return svm_model_binary, svm_model_multiclass, scaler, features, X_train, y_multiclass


# from django.shortcuts import render
# from django.conf import settings
# import numpy as np
# import os
# import matplotlib.pyplot as plt
# from lime.lime_tabular import LimeTabularExplainer


# def prediction(request):
#     # Train models and retrieve necessary components
#     svm_model_binary, svm_model_multiclass, scaler, features, X_train, y_multiclass = train_models()
    
#     lime_binary_path = None
#     lime_multiclass_path = None

#     if request.method == 'POST':
#         # Collect input data from the form
#         try:
#             input_data = {
#                 'pos_0': float(request.POST['pos_0']),
#                 'pos_1': float(request.POST['pos_1']),
#                 'pos_noise_0': float(request.POST['pos_noise_0']),
#                 'pos_noise_1': float(request.POST['pos_noise_1']),
#                 'spd_0': float(request.POST['spd_0']),
#                 'spd_1': float(request.POST['spd_1']),
#                 'spd_noise_0': float(request.POST['spd_noise_0']),
#                 'spd_noise_1': float(request.POST['spd_noise_1']),
#                 'acl_0': float(request.POST['acl_0']),
#                 'acl_1': float(request.POST['acl_1']),
#                 'acl_noise_0': float(request.POST['acl_noise_0']),
#                 'acl_noise_1': float(request.POST['acl_noise_1']),
#                 'hed_0': float(request.POST['hed_0']),
#                 'hed_1': float(request.POST['hed_1']),
#                 'hed_noise_0': float(request.POST['hed_noise_0']),
#                 'hed_noise_1': float(request.POST['hed_noise_1'])
#             }

#             # Normalize the input data
#             input_data_array = np.array(list(input_data.values())).reshape(1, -1)
#             input_data_normalized = scaler.transform(input_data_array)

#             # Predict attack detection and attack type
#             attack_detection_result = svm_model_binary.predict(input_data_normalized)[0]
#             attack_type_result = svm_model_multiclass.predict(input_data_normalized)[0]
#             attack_detection = 'Attack' if attack_detection_result == 1 else 'Benign'

#             # Generate LIME explanations
#             explainer = LimeTabularExplainer(
#                 training_data=X_train,
#                 feature_names=features,
#                 class_names=['Benign', 'Attack'],
#                 mode='classification'
#             )

#             # LIME explanation for binary model
#             explanation_binary = explainer.explain_instance(
#                 input_data_normalized[0],
#                 svm_model_binary.predict_proba
#             )
#             lime_binary_path = os.path.join(settings.MEDIA_ROOT, "lime_binary.png")
#             explanation_binary.save_to_file(lime_binary_path)

#             # LIME explanation for multiclass model
#             explanation_multiclass = explainer.explain_instance(
#                 input_data_normalized[0],
#                 svm_model_multiclass.predict_proba
#             )
#             lime_multiclass_path = os.path.join(settings.MEDIA_ROOT, "lime_multiclass.png")
#             explanation_multiclass.save_to_file(lime_multiclass_path)

#         except Exception as e:
#             return render(request, 'prediction.html', {'error': str(e)})

#         # Render results
#         result = {
#             'attack_detection': attack_detection,
#             'attack_type': attack_type_result,
#             'lime_binary_path': os.path.join(settings.STATICFILES_DIRS, "lime_binary.png"),
#             'lime_multiclass_path': os.path.join(settings.STATICFILES_DIRS, "lime_multiclass.png"),

#         }
#         return render(request, 'prediction.html', {'result':result })

#     # Render the prediction form page
#     return render(request, 'prediction.html')



# from django.shortcuts import render
# import numpy as np
# import pandas as pd
# from sklearn.svm import SVC
# from sklearn.preprocessing import StandardScaler
# from lime.lime_tabular import LimeTabularExplainer
# import shap
# import os
# import matplotlib.pyplot as plt
# from django.conf import settings

# def train_models():
#     # Load Dataset (use your actual dataset path)
#     data = pd.read_csv('dataset.csv')

#     # Select Features and Targets
#     features = ['pos_0', 'pos_1', 'pos_noise_0', 'pos_noise_1',
#                 'spd_0', 'spd_1', 'spd_noise_0', 'spd_noise_1',
#                 'acl_0', 'acl_1', 'acl_noise_0', 'acl_noise_1',
#                 'hed_0', 'hed_1', 'hed_noise_0', 'hed_noise_1']
#     X = data[features]

#     # Binary Classification Target: Attack Detection (0 = Benign, 1 = Attack)
#     y_binary = data['attack']

#     # Multiclass Classification Target: Attack Type Detection
#     y_multiclass = data['attack_type']

#     # Train-Test Split
#     from sklearn.model_selection import train_test_split
#     X_train, X_test, y_train_binary, y_test_binary, y_train_multiclass, y_test_multiclass = train_test_split(
#         X, y_binary, y_multiclass, test_size=0.3, random_state=42
#     )

#     # Normalize Features
#     scaler = StandardScaler()
#     X_train = scaler.fit_transform(X_train)
#     X_test = scaler.transform(X_test)

#     # Train SVM Model for Binary Classification
#     svm_model_binary = SVC(probability=True, kernel='rbf', C=1)
#     svm_model_binary.fit(X_train, y_train_binary)

#     # Train SVM Model for Multiclass Classification
#     svm_model_multiclass = SVC(probability=True, kernel='rbf', C=1)
#     svm_model_multiclass.fit(X_train, y_train_multiclass)

#     return svm_model_binary, svm_model_multiclass, scaler, features, X_train

# def prediction(request):
#     svm_model_binary, svm_model_multiclass, scaler, features, X_train = train_models()
#     result = None

#     if request.method == 'POST':
#         input_data = {
#             'pos_0': float(request.POST['pos_0']),
#             'pos_1': float(request.POST['pos_1']),
#             'pos_noise_0': float(request.POST['pos_noise_0']),
#             'pos_noise_1': float(request.POST['pos_noise_1']),
#             'spd_0': float(request.POST['spd_0']),
#             'spd_1': float(request.POST['spd_1']),
#             'spd_noise_0': float(request.POST['spd_noise_0']),
#             'spd_noise_1': float(request.POST['spd_noise_1']),
#             'acl_0': float(request.POST['acl_0']),
#             'acl_1': float(request.POST['acl_1']),
#             'acl_noise_0': float(request.POST['acl_noise_0']),
#             'acl_noise_1': float(request.POST['acl_noise_1']),
#             'hed_0': float(request.POST['hed_0']),
#             'hed_1': float(request.POST['hed_1']),
#             'hed_noise_0': float(request.POST['hed_noise_0']),
#             'hed_noise_1': float(request.POST['hed_noise_1'])
#         }

#         input_data_array = np.array(list(input_data.values())).reshape(1, -1)
#         input_data_normalized = scaler.transform(input_data_array)

#         # Predictions
#         attack_detection_result = svm_model_binary.predict(input_data_normalized)[0]
#         attack_type_result = svm_model_multiclass.predict(input_data_normalized)[0]
#         attack_detection = 'Attack' if attack_detection_result == 1 else 'Benign'

#         # LIME Explanation (Binary)
#         lime_explainer_binary = LimeTabularExplainer(
#             X_train, feature_names=features, class_names=['Benign', 'Attack'], mode='classification'
#         )
#         lime_exp_binary = lime_explainer_binary.explain_instance(
#             input_data_array[0], svm_model_binary.predict_proba
#         )
#         lime_exp_binary_list = lime_exp_binary.as_list()

#         # LIME Explanation (Multiclass)
#         lime_explainer_multiclass = LimeTabularExplainer(
#             X_train, feature_names=features, class_names=[str(i) for i in np.unique(X_train)], mode='classification'
#         )
#         lime_exp_multiclass = lime_explainer_multiclass.explain_instance(
#             input_data_array[0], svm_model_multiclass.predict_proba
#         )
#         lime_exp_multiclass_list = lime_exp_multiclass.as_list()

#         # SHAP Explanation (Binary)
#         shap_explainer_binary = shap.Explainer(svm_model_binary.predict_proba, X_train)
#         shap_values_binary = shap_explainer_binary(input_data_normalized)

#         # Save SHAP force plot (Binary)
#         shap_plot_path_binary = os.path.join(settings.MEDIA_ROOT, 'shap_plot_binary.png')
#         shap.force_plot(
#             shap_explainer_binary.expected_value[1],
#             shap_values_binary.values[0][:, 1],
#             input_data_normalized[0],
#             feature_names=features,
#             matplotlib=True
#         )
#         plt.savefig(shap_plot_path_binary, bbox_inches='tight')
#         plt.close()

#         # SHAP Explanation (Multiclass)
#         shap_explainer_multiclass = shap.Explainer(svm_model_multiclass.predict_proba, X_train)
#         shap_values_multiclass = shap_explainer_multiclass(input_data_normalized)

#         # Save SHAP force plot (Multiclass)
#         shap_plot_path_multiclass = os.path.join(settings.MEDIA_ROOT, 'shap_plot_multiclass.png')
#         shap.force_plot(
#             shap_explainer_multiclass.expected_value[1],
#             shap_values_multiclass.values[0][:, 1],
#             input_data_normalized[0],
#             feature_names=features,
#             matplotlib=True
#         )
#         plt.savefig(shap_plot_path_multiclass, bbox_inches='tight')
#         plt.close()

#         result = {
#             'attack_detection': attack_detection,
#             'attack_type': attack_type_result,
#             'lime_exp_binary': lime_exp_binary_list,
#             'lime_exp_multiclass': lime_exp_multiclass_list,
#             'shap_plot_binary': os.path.join(settings.MEDIA_URL, 'shap_plot_binary.png'),
#             'shap_plot_multiclass': os.path.join(settings.MEDIA_URL, 'shap_plot_multiclass.png')
#         }

#     return render(request, 'prediction.html', {'result': result})



from django.shortcuts import render
import numpy as np
import joblib
from lime.lime_tabular import LimeTabularExplainer
import os

# Load the models and scaler
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
svm_model_binary = joblib.load(os.path.join(BASE_DIR, "svm_model_binary.pkl"))
svm_model_multiclass = joblib.load(os.path.join(BASE_DIR, "svm_model_multiclass.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "scaler.pkl"))

# Define Features
FEATURES = ['pos_0', 'pos_1', 'pos_noise_0', 'pos_noise_1',
            'spd_0', 'spd_1', 'spd_noise_0', 'spd_noise_1',
            'acl_0', 'acl_1', 'acl_noise_0', 'acl_noise_1',
            'hed_0', 'hed_1', 'hed_noise_0', 'hed_noise_1']


def prediction(request):
    prediction_result = None
    lime_html = None
    if request.method == "POST":
        # Collect input data from the form
        input_data = np.array([float(request.POST.get(feature, 0)) for feature in FEATURES]).reshape(1, -1)

        # Normalize the input data
        input_data_normalized = scaler.transform(input_data)

        # Predict Binary Classification
        attack_detection_result = svm_model_binary.predict(input_data_normalized)[0]
        attack_detection = "Attack" if attack_detection_result == 1 else "Benign"

        # Predict Multiclass Classification
        attack_type_result = svm_model_multiclass.predict(input_data_normalized)[0]

        # Generate LIME Explanation
        lime_explainer = LimeTabularExplainer(
            scaler.transform(np.array([[0] * len(FEATURES)] * 10)),  # Placeholder training data
            feature_names=FEATURES, class_names=['Benign', 'Attack'], mode='classification'
        )
        lime_exp_binary = lime_explainer.explain_instance(
            input_data_normalized[0], svm_model_binary.predict_proba
        )
        lime_html = lime_exp_binary.as_html()

        # Prepare the prediction results
        prediction_result = {
            "attack_detection": attack_detection,
            "attack_type": str(attack_type_result),
        }

    return render(request, "prediction.html", {
        "features": FEATURES,
        "prediction_result": prediction_result,
        "lime_html": lime_html,
    })

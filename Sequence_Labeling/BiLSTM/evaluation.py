from utils import LoadData
from utils import load_checkpoint
import torch
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import numpy as np
from torchcrf import CRF
from model import AttentionBiLSTM_Seqence
import torchtext
from seq_scorer import score

train_iter, valid_iter, test_iter, TAGS, TEXT, fields = LoadData()

device = "cuda"
count = 0
    
def check_infer():
    with open("/home/ubuntu/NLPCourse/Assignment/Sequence_Labeling/test.label", "r", encoding="utf-8") as fr:
        text_infer = fr.read().splitlines()
    with open("/home/ubuntu/NLPCourse/Assignment/Sequence_Labeling/predict.txt", "r", encoding="utf-8") as fr1:
        text_infer1 = fr1.read().splitlines()
    for t, t1 in zip(text_infer, text_infer1):
        
        assert len(t.split(" ") ) - 1 == len(t1.split(" "))

def evaluate(model):
        # This method applies the trained model to a list of sentences.
        
        # First, create a torchtext Dataset containing the sentences to tag.
        crf = CRF(len(TAGS.vocab)).to(device)

        model.eval()
        out = []
        with open("/home/ubuntu/NLPCourse/Assignment/Sequence_Labeling/predict_bilstm.txt", "w+", encoding="utf-8") as fw:
            with torch.no_grad():
                for (text,tags), _ in test_iter:

                    output = model(text,tags)
                    top_predictions = crf.decode(output)

                    predicted_tags = [TAGS.vocab.itos[t] for t in top_predictions[0] ]

                    fw.write(" ".join(predicted_tags) + "\n")
                    print(predicted_tags)


if __name__ == '__main__':

    best_model = AttentionBiLSTM_Seqence(TEXT, TAGS, n_embed=300, n_hidden=128).to("cuda")

    load_checkpoint('Seq_BiLSTM.pt', best_model)

    evaluate(best_model)

    check_infer()

    key = [str(line).rstrip('\n') for line in open("../data/test.label")]
    prediction = [str(line).rstrip('\n') for line in open("../data/predict.txt")]
    score(key, prediction, verbose=True)

# Precision = 72.72727272727273 , Recall = 4.4692737430167595 , F1 = 8.421052631578947  30 epoch
# Precision = 54.54545454545455 , Recall = 100.0 , F1 = 70.58823529411765    50 epoch
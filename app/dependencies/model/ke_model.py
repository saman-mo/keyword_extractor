from hydra import compose, initialize
import pytorch_lightning as pl
from transformers import BertConfig, BertForTokenClassification, BertForMaskedLM
import torch
import torch.nn as nn
from torchmetrics.classification import MultilabelPrecision, MultilabelF1Score, BinaryF1Score, BinaryPrecision


LABELS = ['job-title', 'location', 'company', 'skills', 
          'job-title-sentence', 'location-sentence', 
          'company-sentence', 'skill-paragraph']


with initialize(version_base=None, config_path="."):
    cfg = compose(config_name="model_config.yaml")

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


class KeywordExtractionModel(pl.LightningModule):
    def __init__(self, num_classes: int = cfg.num_classes,
                 learning_rate: float = cfg.learning_rate):
        super().__init__()
        self.save_hyperparameters()

        self.con = BertConfig.from_pretrained(cfg.pretrained_model_path, num_labels=num_classes, 
            output_attentions=False, hidden_dropout_prob=cfg.hidden_dropout_prob, 
            output_hidden_states=False, classifier_dropout=cfg.classifier_dropout, 
            attention_probs_dropout_prob=cfg.attention_probs_dropout_prob)
        self.transformer = BertForTokenClassification.from_pretrained(
            cfg.pretrained_model_path, config=self.con)

        self.transformer.resize_token_embeddings(cfg.vocab_size)

        self.num_classes = num_classes

        self.cls_wts = torch.load(cfg.cls_wts)
        self.learning_rate = learning_rate
        self.batch_size = None
        self.loss_function = nn.BCELoss(weight=self.cls_wts)
        self.sigmoid = nn.Sigmoid()
        self.train_f1_score = MultilabelF1Score(num_classes, average=None, 
            multidim_average='global', threshold=cfg.metrics_threshold)
        self.train_percision = MultilabelPrecision(num_classes, average=None, 
            multidim_average='global', threshold=cfg.metrics_threshold)
        self.val_f1_score = MultilabelF1Score(num_classes, average=None, 
            multidim_average='global', threshold=cfg.metrics_threshold)
        self.val_percision = MultilabelPrecision(num_classes, average=None,
            multidim_average='global', threshold=cfg.metrics_threshold) 
        self.best_percision = 0.00
        self.count = -1

    def forward(self, input_ids, att_masks, token_type_ids):
        self.batch_size = input_ids.shape[0]
        logits = self.transformer(input_ids=input_ids, attention_mask=att_masks,
            token_type_ids=token_type_ids).logits
        return self.sigmoid(logits)





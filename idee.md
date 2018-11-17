
matching colonne con TFIDF + mse pesato (colonna)

drop cose la cui |sum - 100g| >= 10g aka drop rows with more than 10% error
suddivisione in categorie
estrazione delle distribuzioni dei valori e sanitizzazzione degli outlier

match usando sempre TFIDF + mse pesato (riga) tra dataset deve essere una relazione di equivalenza -> riflessiva, transitiva, simmetrica
questo la tfidf + mse pesato e' gia' riflessiva e simmetrica
transitiva  -> ricerca del sottografo connesso a costo minimo a massima cardinalita' (#sottografo <= #Datasets)
si puo' impostarlo come un problema di ricerca operativa intero su grafo pesato non direzionato (in quanto la distanza e' simmetrica),


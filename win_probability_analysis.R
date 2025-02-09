#####

# Cosa serve per vincere nel basket?

# Per cominciare, carichiamo i dati 
data <- read.table("data/team_stats.txt", header = T)
head(data)
# Franchigie considerate
franchigie <- c("ATL", "BOS", "BKN", "CHA", "CHI", "CLE", "DAL", "DEN", "DET", "GSW",
                "HOU", "IND", "LAC", "LAL", "MEM", "MIA", "MIL", "MIN", "NOP", "NYK",
                "OKC", "ORL", "PHI", "PHX", "POR", "SAC", "SAS", "TOR", "UTA", "WAS")


# Come primo modello consideriamo come esplicative le componenti principali derivanti dai 4 fattori
apply(data[, 6:9], 2, sd)
# La percentuale di palle perse ha una varianza molto diversa dalle altre metriche. E' necessario standardizzare i dati
pca <- prcomp(data[, 6:9], scale. = TRUE)
# Guardiamo la percentuale di varianza spiegata cumulata per capire quante componenti utilizzare
cumsum((pca$sdev ^ 2) / sum(pca$sdev ^ 2))
# 2 componenti principali spiegano una il 74% della varianza totale
X.0 <- pca$x[, c(1, 2)]

# Ora che ho ricavato le esplicative, posso procedere con la costruzione del modello
win.prob.glm.pca <- glm(cbind(data[, 1], data[, 2]) ~ X.0[, 1] + X.0[, 2], family = binomial)
summary(win.prob.glm.pca)
# Il coefficiente della seconda variabile canonica è non significativo. Anche l'intercetta risulta non significativa, con il relativo coefficiente sostanzialmente degenere in 0. Aggiorniamo il modello
win.prob.glm.pca <- update(win.prob.glm.pca, . ~ . - X.0[, 2])
summary(win.prob.glm.pca)
# Guardando la devianza residua non siamo soddisfatti dell'adattamento del modello. Il modello corrente, con soli 2 parametri in più rispetto al modello nullo, spiega molto di più di quest'ultimo. Tuttavia viene rifiutata l'ipotesi di adattamento del modello corrente rispetto a quello nullo
# H0: modello nullo   H1: modello corrente
pchisq(win.prob.glm.pca$null.deviance - win.prob.glm.pca$deviance, 
       win.prob.glm.pca$df.null - win.prob.glm.pca$df.residual, lower.tail = FALSE)
# H0 : modello corrente  H1: modello saturo
pchisq(win.prob.glm.pca$deviance, win.prob.glm.pca$df.residual, lower.tail = FALSE)
# Compariamo i valori osservati con i valori previsti dal modello. L'asse x indica le squadre in ordine alfabetico
diff.pca <- data$W - fitted(win.prob.glm.pca) * 82
plot(1:30, diff.pca, type = "h", xlab = "NBA teams", ylab = "W.obs - W.exp",
     ylim = c(-25, 20), xaxt = "n", main = "Adattamento modello logit PCA")
abline(h = 0, lty = 2)
axis(1, at = 1:30, labels = franchigie, las = 2, cex.axis = 0.8)
# L'adattamento non è sicuramente dei migliori. Il modello, utilizzando solamente due esplicative, deve mediare le percentuali osservate e nei casi estremi (numero di vittorie molto alto o molto basso) dà risultati fuorvianti

# Costruiamo un altro modello prendendo come esplicative i 4 fattori senza applicare la PCA. La PCA comporta infatti una riduzione della dimensionalità: il modello che ne deriva ha, oltre all'intercetta, 2 parametri (numero di PC considerate) invece che 4. Vediamo se, con più esplicative, il modello si adatta meglio ai dati
win.prob.glm.0 <- glm(cbind(W, L) ~ eFG. + TOV. + ORB. + FTR, 
                      family = binomial, data = data)
summary(win.prob.glm.0)
# Il modello appena costruito fornisce un adattamento migliore ai dati rispetto a quello visto in precedenza
compare.matrix <- matrix(data = c(win.prob.glm.pca$aic, win.prob.glm.0$aic,
      BIC(win.prob.glm.pca), BIC(win.prob.glm.0)), nrow = 2, byrow = TRUE)
colnames(compare.matrix) <- c("PCA", "4Factors")
row.names(compare.matrix) <- c("AIC", "BIC")
compare.matrix
# Anche qui confrontiamo valori osservati e predetti
diff.4f <- data$W - fitted(win.prob.glm.0) * 82
plot(1:30, diff.4f, type = "h", xlab = "NBA teams", ylab = "W.obs - W.exp",
     ylim = c(-25, 20), xaxt = "n", main = "Adattamento modello logit 4 factors")
abline(h = 0, lty = 2)
axis(1, at = 1:30, labels = franchigie, las = 2, cex.axis = 0.8)
# L'adattamento è visibilmente migliorato, tuttavia non siamo soddisfatti rispetto a ciò che otteniamo con il modello saturo
# H0: modello corrente   H1: modello saturo
pchisq(win.prob.glm.0$deviance, win.prob.glm.0$df.residual, lower.tail = FALSE)

# Considerata l'importanza che hanno il tiro da tre punti e il pace (ritmo di gioco) nel basket moderno costruiamo un nuovo modello aggiungendo 3 esplicative: numero di tiri da tre segnati, numero di tiri da tre tentati e possessi per partita
win.prob.glm <- glm(cbind(W, L) ~ ., family = binomial, data = data)
summary(win.prob.glm)
# Il coefficiente relativo ai tiri da tre punti tentati a partita è non significativo. Aggiorniamo il modello
win.prob.glm <- update(win.prob.glm, . ~ . - FG3A.GP)
summary(win.prob.glm)
# L'intercetta risulta non significativa
win.prob.glm <- update(win.prob.glm, . ~ . - 1)
summary(win.prob.glm)
# L'adattamento rispetto ai modelli precedenti è migliorato
compare.matrix <- cbind(compare.matrix, c(win.prob.glm$aic, BIC(win.prob.glm)))
colnames(compare.matrix) <- c("PCA", "4Factors", "4Factors + 3PTShot")
compare.matrix
# Accettiamo l'ipotesi nulla ad un livello di significatività del 5%
# H0: modello corrente   H1: modello saturo
pchisq(win.prob.glm$deviance, win.prob.glm$df.residual, lower.tail = FALSE)
# Grafico valori previsti e osservati
diff.4f.mod <- data$W - fitted(win.prob.glm) * 82
plot(1:30, diff.4f.mod, type = "h", xlab = "NBA teams", ylab = "W.obs - W.exp",
     ylim = c(-25, 20), xaxt = "n", main = "Adattamento modello logit 4 factors + pace + 3P shot")
abline(h = 0, lty = 2)
axis(1, at = 1:30, labels = franchigie, las = 2, cex.axis = 0.8)
# Media della discrepanza tra il numero di vittorie effettivo e il numero di vittorie stimato
mean(abs(residuals(win.prob.glm, type = "response"))) * 82
# Metodo alternativo
mean(abs(data$W - fitted(win.prob.glm) * 82))
sd(abs(data$W - fitted(win.prob.glm) * 82))
# Ciò significa che in media sbaglio la previsione delle vittorie di 4 unità
# Non vi è struttura di dipendenza tra i valori predetti e i residui
plot(win.prob.glm, which = 1)

# Le possibili interazioni aggiuntive risultano non significative
add1(win.prob.glm, . ~ . + (.)^2, test = "Chisq") 

# In conclusione, il migliore dei modelli considerati è quello con le seguenti esplicative: tiri da tre punti segnati a partita, possessi a partita, percentuale effettiva, percentuale di palle perse, percentuale di rimbalzi offensivi e numero di tiri liberi rispetto ai tiri dal campo.















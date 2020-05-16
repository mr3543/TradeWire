# TradeWire

TradeWire allows you to submit an online news article and find publicly traded companies whose business operations are related to the content of that news article. TradeWire utilizes Latent Dirichlet Allocation as its document similarity engine. Future plans involve getting rid of LDA in favor of BERT embeddings to match sentences in the submitted article to sentences in our database. For now visit the site at (http://www.tradewire.xyz). 

Our dataset consists of the text portion of the 10-K filing of over 4000 companies. Currently we are supporting search on ~450 of the largest US companies. We extracted the "Business" and "Risk Factors" secitons from each 10-K. These sections provide a high level overview of the company's business operations. 

Example:

Submitting the article https://www.cnn.com/2020/05/03/health/coronavirus-vaccine-never-developed-intl/index.html, an article about a potential coronavirus vaccine returns 

1. mrk: Merck and Co., pharmaceutical company
2. bmy: Bristol-Myers Squibb, pharmaceutical company
3. alxn: Alexion, pharmaceutical company
...

Submitting https://www.cnn.com/2020/05/03/success/landlords-rent-may-coronavirus/index.html, an article about landlords and housing rentals returns

1. amt: American Tower Corp, real estate investment trust
2. cci: Crown Castle International, real estate investment trust
3. kim: Kimco Realty Corp, real estate investment trust
...

`/notebooks` contains notebooks used to scrape the SEC database and train the topic model. `/web` contains our web endpoints and templates. 





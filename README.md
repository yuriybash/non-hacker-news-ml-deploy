## non-hacker-news-ml-deploy

simple app to serve prediction (technical vs. nontechnical classification) requests for Hacker News articles.

See [this](https://github.com/yuriybash/non-hacker-news-ml) repo for the model implementation, and [this](https://github.com/yuriybash/non-hacker-news-chrome) repo for the chrome extension details.

And most importantly, see go [here]() to download and try the extension out yourself!

## Making a request

```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"data":[["python hacker c++", "github"], ["trump wall politics", "nytimes"]]}' \
  https://XXXXXX.execute-api.us-east-1.amazonaws.com/dev
```

returns

```
{
    "prediction": [
        [0.9929274514831136, 0.007072548516887224],
        [0.29853598715795543, 0.7014640128420446]
    ]
}
```

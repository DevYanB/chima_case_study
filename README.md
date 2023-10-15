To run docker:
`docker-compose up --build`
Running into some frontend deployment issues, however, so do run locally:

Install all req's:
`pip install -r requirements.txt`

Spin up a postgres DB (however you want) and replace it in dev-secrets.rc
`source dev-secrets.rc`

```dotnetcli
$ python app.py
```

```dotnetcli
$ cd chima-app
$ npm start
```

To have it work, you need to setup an inference endpoint with huggingface (as I am waiting for sagemaker allowance)
visit [this link](https://ui.endpoints.huggingface.co/devyanbiswas/new?repository=daryl149%2Fllama-2-7b-chat-hf) for an example for running this open source endpoint.
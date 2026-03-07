# We provide the advanced preproc tokenization for reranking.
from BCEmbedding.tools.langchain import BCERerank

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS

from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain.retrievers import ContextualCompressionRetriever

# init embedding model
embedding_model_name = "maidalun1020/bce-embedding-base_v1"
embedding_model_kwargs = {"device": "cpu"}
embedding_encode_kwargs = {"batch_size": 32, "normalize_embeddings": True}

embed_model = HuggingFaceEmbeddings(
    model_name=embedding_model_name,
    model_kwargs=embedding_model_kwargs,
    encode_kwargs=embedding_encode_kwargs,
)

reranker_model_name = "maidalun1020/bce-reranker-base_v1"
# reranker_model = RerankerModel(model_name_or_path=reranker_model_name)

# init documents
documents = PyPDFLoader("assets/pdfs/en/2025-02-04-wifi-speed-en.pdf").load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
texts = text_splitter.split_documents(documents)

# example 1. retrieval with embedding and reranker
retriever = FAISS.from_documents(
    texts, embed_model, distance_strategy=DistanceStrategy.MAX_INNER_PRODUCT
).as_retriever(
    search_type="similarity", search_kwargs={"score_threshold": 0.3, "k": 10}
)

reranker = BCERerank()

compression_retriever = ContextualCompressionRetriever(
    base_compressor=reranker, base_retriever=retriever
)

response = compression_retriever.get_relevant_documents("What is Llama 2?")

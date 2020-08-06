from concurrent import futures
import datetime
import itertools
import requests
from urllib.parse import urlparse


class Measurement:
  def __init__(self, parallelism):
    self.parallelism = parallelism

  def response_size(self, urls):
    """Returns (url, size) pairs for all provided URLs as a generator"""
    return self.__async(urls, lambda response: len(response.content))

  def response_time(self, urls):
    """Returns (url, response time) pairs for all provided URLs as a generator"""
    return self.__async(urls, lambda response: response.elapsed)

  def average_response_time(self, urls):
    """Returns (domain, average response time) pairs as a generator"""
    by_domain = {}
    for url, response in self.response_time(urls):
      domain = ".".join(urlparse(url).netloc.split(".")[-2:])
      if domain not in by_domain:
        by_domain[domain] = []
      by_domain[domain].append(response)

    return (
      (domain, sum(response_times, datetime.timedelta())/len(response_times))
      for (domain, response_times) in by_domain.items()
    )

  def __async(self, urls, operation):
    with futures.ThreadPoolExecutor(max_workers=self.parallelism) as executor:
      pairs = [
        (url, executor.submit(lambda: operation(requests.get(url))))
        for url in urls
      ]

    return (
      (url, future.result())
      for (url, future) in pairs
    )

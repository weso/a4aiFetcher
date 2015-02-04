from infrastructure.mongo_repos.indicator_repository import IndicatorRepository
from infrastructure.mongo_repos.observation_repository import ObservationRepository

__author__ = 'Miguel'


class Ranker(object):

    def __init__(self, log, config):
        self._log = log
        self._config = config
        self._indicator_repo, self._observation_repo = self.initialize_repositories()

    def initialize_repositories(self):
        indicator_repo = IndicatorRepository(self._config.get("CONNECTION", "MONGO_IP"))
        observation_repo = ObservationRepository(self._config.get("CONNECTION", "MONGO_IP"))
        return indicator_repo, observation_repo

    def run(self):
        self.rank_observations()
        self.rank_emerging_countries_observations()
        self.rank_developing_countries_observations()

    def rank_observations(self):
        indicators = self._indicator_repo.find_indicators()
        for indicator in indicators:
            observations = self._observation_repo.find_observations(indicator_code=indicator.indicator)
            ordered = sorted(observations, key=lambda observation: observation.value)
            rank = len(ordered)
            for obs in ordered:
                self._observation_repo.update_observation_ranking(obs, rank)
                rank -= 1

    def rank_emerging_countries_observations(self):
        indicators = self._indicator_repo.find_indicators()
        for indicator in indicators:
            emerging_observations = self._observation_repo.find_observations(indicator_code=indicator.indicator,
                                                                             area_type="Emerging")
            emerging_ordered = sorted(emerging_observations, key=lambda observation: observation.value)
            rank_emerging = len(emerging_ordered)
            for emerging_obs in emerging_ordered:
                self._observation_repo.update_observation_ranking_type(emerging_obs, rank_emerging)
                rank_emerging -= 1

    def rank_developing_countries_observations(self):
        indicators = self._indicator_repo.find_indicators()
        for indicator in indicators:
            developing_observations = self._observation_repo.find_observations(indicator_code=indicator.indicator,
                                                                               area_type="Developing")
            developing_ordered = sorted(developing_observations, key=lambda observation: observation.value)
            rank_developing = len(developing_ordered)
            for developing_obs in developing_ordered:
                self._observation_repo.update_observation_ranking_type(developing_obs, rank_developing)
                rank_developing -= 1
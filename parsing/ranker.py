from infrastructure.mongo_repos.indicator_repository import IndicatorRepository
from infrastructure.mongo_repos.observation_repository import ObservationRepository

__author__ = 'Miguel'


class Ranker(object):

    def __init__(self, log, config):
        self._log = log
        self._config = config
        self._indicator_repo, self._observation_repo = self._initialize_repositories()

    def _initialize_repositories(self):
        indicator_repo = IndicatorRepository(self._config.get("CONNECTION", "MONGO_IP"))
        observation_repo = ObservationRepository(self._config.get("CONNECTION", "MONGO_IP"))
        return indicator_repo, observation_repo

    def run(self):
        self._log.info("Ranking observations")
        print "Ranking observations"
        self._rank_observations()
        self._rank_emerging_countries_observations()
        self._rank_developing_countries_observations()

    def _rank_observations(self):
        self._log.info("\tRanking all countries observations...")
        print "\tRanking all countries observations..."
        indicators = self._indicator_repo.find_indicators()
        for indicator in indicators:
            observations = self._observation_repo.find_observations(indicator_code=indicator.indicator)
            ordered = sorted(observations, key=lambda observation: observation.value, reverse=True)
            rank = 1
            for obs in ordered:
                if obs.value != "":
                    self._observation_repo.update_observation_ranking(obs, rank)
                    rank += 1

    def _rank_emerging_countries_observations(self):
        self._log.info("\tRanking observations by type of emerging countries")
        print "\tRanking observations by type of emerging countries"
        indicators = self._indicator_repo.find_indicators()
        for indicator in indicators:
            emerging_observations = self._observation_repo.find_observations(indicator_code=indicator.indicator,
                                                                             area_type="Emerging")
            emerging_ordered = sorted(emerging_observations, key=lambda observation: observation.value, reverse=True)
            rank_emerging = 1
            for emerging_obs in emerging_ordered:
                if emerging_obs.value != "":
                    self._observation_repo.update_observation_ranking_type(emerging_obs, rank_emerging)
                    rank_emerging += 1

    def _rank_developing_countries_observations(self):
        self._log.info("\tRanking observations by type of developing countries")
        print "\tRanking observations by type of developing countries"
        indicators = self._indicator_repo.find_indicators()
        for indicator in indicators:
            developing_observations = self._observation_repo.find_observations(indicator_code=indicator.indicator,
                                                                               area_type="Developing")
            developing_ordered = sorted(developing_observations, key=lambda observation: observation.value, reverse=True)
            rank_developing = 1
            for developing_obs in developing_ordered:
                if developing_obs.value != "":
                    self._observation_repo.update_observation_ranking_type(developing_obs, rank_developing)
                    rank_developing += 1
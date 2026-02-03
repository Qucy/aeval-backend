import json
from pathlib import Path
from typing import List, Optional

from app.models.dataset import Dataset
from app.models.metric import Metric
from app.models.scenario import Scenario
from app.models.agent import AgentModel


class DataService:
    """Service for loading and caching evaluation data from JSON files."""

    def __init__(self, data_dir: Path | None = None) -> None:
        """Initialize the data service with a data directory."""
        from app.config import settings

        self.data_dir = Path(data_dir or settings.data_dir)
        self._datasets: Optional[List[Dataset]] = None
        self._metrics: Optional[List[Metric]] = None
        self._scenarios: Optional[List[Scenario]] = None
        self._agents: Optional[List[AgentModel]] = None

    async def load_datasets(self) -> List[Dataset]:
        """Load datasets from JSON file with caching.

        Raises:
            FileNotFoundError: If datasets.json file not found
            ValueError: If JSON is invalid or data validation fails
        """
        if self._datasets is None:
            file_path = self.data_dir / "datasets.json"
            try:
                with open(file_path) as f:
                    data = json.load(f)
                    self._datasets = [Dataset(**d) for d in data]
            except FileNotFoundError:
                raise FileNotFoundError(f"Data file not found: {file_path}")
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON in {file_path}: {e}")
            except Exception as e:
                raise ValueError(f"Data validation error in {file_path}: {e}")
        return self._datasets

    async def load_metrics(self) -> List[Metric]:
        """Load metrics from JSON file with caching.

        Raises:
            FileNotFoundError: If metrics.json file not found
            ValueError: If JSON is invalid or data validation fails
        """
        if self._metrics is None:
            file_path = self.data_dir / "metrics.json"
            try:
                with open(file_path) as f:
                    data = json.load(f)
                    self._metrics = [Metric(**m) for m in data]
            except FileNotFoundError:
                raise FileNotFoundError(f"Data file not found: {file_path}")
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON in {file_path}: {e}")
            except Exception as e:
                raise ValueError(f"Data validation error in {file_path}: {e}")
        return self._metrics

    async def load_scenarios(self) -> List[Scenario]:
        """Load scenarios from JSON file with caching.

        Raises:
            FileNotFoundError: If scenarios.json file not found
            ValueError: If JSON is invalid or data validation fails
        """
        if self._scenarios is None:
            file_path = self.data_dir / "scenarios.json"
            try:
                with open(file_path) as f:
                    data = json.load(f)
                    self._scenarios = [Scenario(**s) for s in data]
            except FileNotFoundError:
                raise FileNotFoundError(f"Data file not found: {file_path}")
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON in {file_path}: {e}")
            except Exception as e:
                raise ValueError(f"Data validation error in {file_path}: {e}")
        return self._scenarios

    async def load_agents(self) -> List[AgentModel]:
        """Load agents from JSON file with caching.

        Raises:
            FileNotFoundError: If agents.json file not found
            ValueError: If JSON is invalid or data validation fails
        """
        if self._agents is None:
            file_path = self.data_dir / "agents.json"
            try:
                with open(file_path) as f:
                    data = json.load(f)
                    self._agents = [AgentModel(**a) for a in data]
            except FileNotFoundError:
                raise FileNotFoundError(f"Data file not found: {file_path}")
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON in {file_path}: {e}")
            except Exception as e:
                raise ValueError(f"Data validation error in {file_path}: {e}")
        return self._agents

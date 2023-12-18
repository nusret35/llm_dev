from typing import TYPE_CHECKING, Any, Dict, Iterator, List, Optional, Union, Tuple

from typing_extensions import Unpack

from replicate import identifier
from replicate.exceptions import ModelError
from replicate.model import Model
from replicate.prediction import Prediction
from replicate.schema import make_schema_backwards_compatible
from replicate.version import Version, Versions
from replicate.client import Client
if TYPE_CHECKING:
    from replicate.client import Client
    from replicate.identifier import ModelVersionIdentifier
    from replicate.prediction import Predictions


class Subclass(Client) :
    def run_model(
        client: "Client",
        ref: Union["Model", "Version", "ModelVersionIdentifier", str],
        input: Optional[Dict[str, Any]] = None,
        **params: Unpack["Predictions.CreatePredictionParams"],
    ) -> Tuple[Any, Any]:  # noqa: ANN401
        """
        Run a model and wait for its output.
        """

        version, owner, name, version_id = identifier._resolve(ref)

        if version_id is not None:
            prediction = client.predictions.create(
                version=version_id, input=input or {}, **params
            )
        elif owner and name:
            prediction = client.models.predictions.create(
                model=(owner, name), input=input or {}, **params
            )
        else:
            raise ValueError(
                f"Invalid argument: {ref}. Expected model, version, or reference in the format owner/name or owner/name:version"
            )

        if not version and (owner and name and version_id):
            version = Versions(client, model=(owner, name)).get(version_id)

        if version and (iterator := _make_output_iterator(version, prediction)):
            return iterator

        prediction.wait()

        if prediction.status == "failed":
            raise ModelError(prediction.error)

        return prediction.output,prediction.metrics



def _make_output_iterator(
    version: Version, prediction: Prediction
) -> Optional[Iterator[Any]]:
    schema = make_schema_backwards_compatible(
        version.openapi_schema, version.cog_version
    )
    output = schema["components"]["schemas"]["Output"]
    if output.get("type") == "array" and output.get("x-cog-array-type") == "iterator":
        return prediction.output_iterator()

    return None


__all__: List = []

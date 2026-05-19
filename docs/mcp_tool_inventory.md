# Phoenix MCP Tool Inventory

Sources checked: Arize Phoenix `js/packages/phoenix-mcp/src` on `main`, including `index.ts`, `promptTools.ts`, `projectTools.ts`, `spanTools.ts`, `datasetTools.ts`, `experimentTools.ts`, and `supportTools.ts`. [Certain]

The source registration calls are treated as authoritative when the README disagrees. [Certain]

## CONFIRMED

- `list-prompts`: input `limit`; returns prompt metadata from `/v1/prompts`. [Certain]
- `get-latest-prompt`: input `prompt_identifier`; returns the latest prompt version from `/v1/prompts/{prompt_identifier}/latest`. [Certain]
- `get-prompt-by-identifier`: input `prompt_identifier`; returns the latest prompt payload from `/v1/prompts/{prompt_identifier}/latest`. [Certain]
- `get-prompt-version`: input `prompt_version_id`; returns one prompt version from `/v1/prompt_versions/{prompt_version_id}`. [Certain]
- `list-prompt-versions`: inputs `prompt_identifier`, optional `limit`; returns prompt versions from `/v1/prompts/{prompt_identifier}/versions`. [Certain]
- `get-prompt-version-by-tag`: inputs `prompt_identifier`, `tag_name`; returns the tagged prompt version from `/v1/prompts/{prompt_identifier}/tags/{tag_name}`. [Certain]
- `list-prompt-version-tags`: inputs `prompt_version_id`, optional `limit`; returns tags from `/v1/prompt_versions/{prompt_version_id}/tags`. [Certain]
- `add-prompt-version-tag`: inputs `prompt_version_id`, `name`, optional `description`; writes a tag through `/v1/prompt_versions/{prompt_version_id}/tags`. [Certain]
- `upsert-prompt`: inputs `name`, optional `description`, `template`, `model_provider`, `model_name`, `temperature`; creates a Phoenix prompt version and returns the created prompt payload. [Certain]
- `list-projects`: inputs optional `limit`, `cursor`, `includeExperimentProjects`; returns project metadata from `/v1/projects`. [Certain]
- `get-spans`: inputs `projectName`, optional time range, cursor, and limit; returns spans plus `nextCursor` from `/v1/projects/{project_identifier}/spans`. [Certain]
- `get-span-annotations`: inputs `projectName`, `spanIds`, optional annotation filters, cursor, and limit; returns annotations plus `nextCursor` from `/v1/projects/{project_identifier}/span_annotations`. [Certain]
- `list-datasets`: input `limit`; returns dataset metadata from `/v1/datasets`. [Certain]
- `get-dataset-examples`: input `datasetId`; returns dataset examples from `/v1/datasets/{id}/examples`. [Certain]
- `get-dataset-experiments`: input `datasetId`; returns experiments from `/v1/datasets/{dataset_id}/experiments`. [Certain]
- `add-dataset-examples`: inputs `datasetName` and examples with input, output, and optional metadata; appends examples through `/v1/datasets/upload`. [Certain]
- `list-experiments-for-dataset`: input `dataset_id`; returns experiments from `/v1/datasets/{dataset_id}/experiments`. [Certain]
- `get-experiment-by-id`: input `experiment_id`; returns experiment metadata plus JSON experiment data from `/v1/experiments/{experiment_id}` and `/v1/experiments/{experiment_id}/json`. [Certain]

## MISSING FROM USER'S LIST

- `phoenix-support`: input `query`; calls the Phoenix support service and returns text guidance about Phoenix, OpenInference, or related topics. [Certain]

## NOT IN SERVER

- `get-prompt`: not registered by the current `promptTools.ts` source. [Certain]
- `get-project`: not registered by the current `projectTools.ts` source. [Certain]
- `list-traces`: not registered by the current `spanTools.ts` source or `index.ts` wiring. [Certain]
- `get-trace`: not registered by the current `spanTools.ts` source or `index.ts` wiring. [Certain]
- `list-sessions`: no sessions tool module is wired in `index.ts`. [Certain]
- `get-session`: no sessions tool module is wired in `index.ts`. [Certain]
- `list-annotation-configs`: no annotation config tool module is wired in `index.ts`. [Certain]
- `get-dataset`: not registered by the current `datasetTools.ts` source. [Certain]

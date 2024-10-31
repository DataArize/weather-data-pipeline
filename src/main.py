from apache_beam.io.external.gcp.pubsub import ReadFromPubSub
from apache_beam.options.pipeline_options import PipelineOptions, SetupOptions
from apache_beam.portability.api.org.apache import beam

from src.utilities.logger import logger


class CustomPipelineOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):

        parser.add_argument('--input_path', required=True, help='Path to the input CSV file in GCS')
        parser.add_argument('--output_table', required=True,
                            help='BigQuery output table in the format project_id.dataset_id.table_id')
        parser.add_argument('--topic', required=True,
                            help='Pubsub topic name')
        parser.add_argument('--subscription', required=True,
                            help='Pubsub subscription name')


def run(argv=None):

    pipeline_options = PipelineOptions(argv)
    custom_options = pipeline_options.view_as(CustomPipelineOptions)
    try:
        project_id, dataset_id, table_id = custom_options.output_table.split('.')
    except ValueError as e:
        logger.error(
            f"Invalid output table format: {custom_options.output_table}. Expected format: project_id.dataset_id.table_id")
        return

    pipeline_options.view_as(SetupOptions).save_main_session = True
    pipeline = beam.Pipeline(options=pipeline_options)
    (pipeline
        | 'Read CSV File' >>
            ReadFromPubSub(
                topic=pipeline_options.topic,
                subscription=pipeline_options.subscription,
            )
        | "Decode message" >> beam.Map(lambda x: x.decode("utf-8"))
        | "Process message" >> beam.Map(lambda msg: print("Processing:", msg))
    )

    pipeline.run().wait_until_finish()

if __name__ == '__main__':
    logger.info("Starting the weather-data-pipeline")
    run()
    logger.info("weather-data-pipeline execution completed")


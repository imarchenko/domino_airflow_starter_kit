from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from domino import Domino
from airflow.models import Variable
# Initialize Domino API object with the api_key and host
api_key=Variable.get("DOMINO_USER_API_KEY")
host=Variable.get("DOMINO_API_HOST")
domino = Domino("jphelps/Airflow_RNATOY",api_key,host)
# Parameters to DAG object:
default_args = {
    'owner': 'domino',
    'depends_on_past': False,
    'start_date': datetime(2020, 11, 11),
    'retries': 1,
    'retry_delay': timedelta(minutes=.5),
    'end_date': datetime(2020, 12, 30),
}
# Instantiate a DAG
dag = DAG('RNATOY', description='Execute Airflow DAG in Domino',default_args=default_args,schedule_interval=timedelta(days=1),catchup=False)
# Define Task instances in Airflow to kick off Jobs in Domino
t1 = PythonOperator(task_id='build_genome_index', python_callable=domino.runs_start_blocking, dag=dag, op_kwargs={"command":["buildprocess.sh"],"tier":"Medium"})
t2= PythonOperator(task_id='map_genome', python_callable=domino.runs_start_blocking, op_kwargs={"command":["mapping.sh"]}, dag=dag)
t3 = PythonOperator(task_id='generate_transcript', python_callable=domino.runs_start_blocking, op_kwargs={"command":["maketranscript.sh"]}, dag=dag)

# Define your dependencies
t2.set_upstream(t1)
t3.set_upstream(t2)
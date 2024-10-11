import yaml

# Define the configuration for the sales_data project
dbt_config = {
    'name': 'sales_data',
    'version': '1.0.0',
    'profile': 'sales_data',
    'model-paths': ['models'],
    'analysis-paths': ['analyses'],
    'test-paths': ['tests'],
    'seed-paths': ['seeds'],
    'macro-paths': ['macros'],
    'snapshot-paths': ['snapshots'],
    'clean-targets': [
        'target',
        'dbt_packages'
    ],
    'models': {
        'sales_data': {
            'example': {
                '+materialized': 'view'
            }
        }
    }
}

# Write the configuration to a YAML file
with open('dbt_project.yml', 'w') as file:
    yaml.dump(dbt_config, file)

print("DBT project configuration written to dbt_project.yml")

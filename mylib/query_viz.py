from pyspark.sql import SparkSession
import matplotlib.pyplot as plt


# Run a SQL query on a Spark DataFrame and return the result of the query
def query_transform():
    spark = SparkSession.builder.appName("Query").getOrCreate()
    query = (
        """
            SELECT w1.Region, w1.Country, w1.year_2000, w1.year_2010, w1.year_2020, w2.year_2022, AVG(w2.year_2022) OVER(PARTITION BY w1.Region) as avg_year_2022
            FROM wages_1_delta w1
            JOIN wages_2_delta w2 ON w1.Country = w2.Country
            ORDER BY avg_year_2022 DESC, w1.Country
        """
    )
    query_result = spark.sql(query)
    return query_result

# sample viz for project
def viz_1():
    query = query_transform()
    count = query.count()
    if count > 0:
        print(f"Data validation passed. {count} rows available.")
    else:
        print("No data available. Please double check.")

    query_result = query.select("Region", "avg_year_2022").toPandas()

    # Group by 'Region' and calculate the mean of 'avg_year_2022'
    grouped_data = query_result.groupby('Region')['avg_year_2022'].mean().reset_index()

    # Create a bar chart with the grouped data
    grouped_data.plot(kind='bar', x='Region', y='avg_year_2022', color='cyan')

    # Set labels and title
    plt.xlabel("Region")
    plt.ylabel("Average Wages in 2022")
    plt.title("Average Wages in 2022 by Region")

    # Show the plot
    plt.show('Avg_2022_Region.png')
    
    query_result = query.select("Region", "avg_year_2022").toPandas()

def viz_2():
    spark = SparkSession.builder.appName("Query").getOrCreate()
    # Write a SQL query to select rows where 'Country' is 'United States' or 'China'
    query = """
    SELECT country, year_2000, year_2010, year_2020 
    FROM wages_1_delta 
    WHERE Country IN ('United States', 'United Kingdom', 'Japan')
    """

    # Execute the SQL query
    query_result = spark.sql(query)

    # Convert the result to a Pandas DataFrame for further operations or visualization
    wages_us_china = query_result.toPandas().set_index('country')

    # Transposing the DataFrame to have years as the X-axis and wages as the Y-axis
    wages_transposed = wages_us_china.transpose()

    # Plotting the line graph
    wages_transposed.plot(kind='line', marker='o')

    # Setting labels and title
    plt.xlabel('Year')
    plt.ylabel('Wages')
    plt.title('Development of Wages Over the Years for the US, UK and Japan')

    # Display the legend
    plt.legend(title='Country')

    # Show the plot
    plt.show('wages_us_china')

if __name__ == "__main__":
    query_transform()
    viz_1()
    viz_2()
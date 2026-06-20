# PySpark UDF Performance Pitfalls and Vectorized UDFs
Why standard python UDFs are slow and how to use Pandas UDFs instead.

- Standard python UDFs require serialization between JVM and Python processes.
- Pandas UDFs use **Apache Arrow** for efficient vectorized calculations.

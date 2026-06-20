# ADF Copy Activity with REST API Pagination
How to handle API pagination inside Azure Data Factory Copy Activity.

## Configuration Details
- **Pagination Rule**: Use `AbsoluteUrl` or `QueryParameters`.
- **Expression Example**: Set header `Range` to `bytes=1000-2000` or use `next_link` cursor loops.
- **Parameters**: Specify dynamic parameters for limit and offsets.

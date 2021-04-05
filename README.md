# Python dashboard template

This is a template for creating dashboards with plotly's Dash for python.

This template covers the following:

- Layout: Cool sidebar layout with page content on right
- Filters: Ability to filter through data
- Color identification: Ability to create plots that takes one column to colorize data
- Callbacks: The callback functions are already defined

## Requirements

- dash and it's dependencies
```
pip3 install dash
```

- pandas
```
pip3 install pandas
```

- PyFladesk
```
pip3 install pyfladesk
```

See also: [requirements](requirements.txt)

## How to use

1. Clone this repository
2. Create plots and tables, put the code into `source/fct_plots.py`
3. Define the pages layouts (`source/pages.py` and `assets/custom.css`)
4. Make edits to the assets folder (for example, change icon)

After creating the pages (as functions), be sure to put links to them in the sidebar (edit `render_sidebar()` function).

`app.py` has some lines that need to be uncommented for deployment.

## columns.json

This file is used to create the filters, each column of your expected dataset should be one entry with the following structure:
- colName: Name of the column (string)
- type: Column type (one of the following: "character", "integer" or "float")
- filterable: Indicator if the column can be used for filtering (1 for yes, 0 for no)
- quickbar: Should the column be on the sidebar? (Left of page)

Other column types can be used, should that be the case, edit `filters.create_filter` accordingly

## License

This template is licensed under MIT license. You are free to do whatever you wish with it, any credits to the author are appreciated.

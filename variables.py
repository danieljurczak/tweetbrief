STYLE = """
        body {
            margin: 0;
            height:297mm;
            width:210mm;
            font-family: monospace;
        }
        @page {
            size: 210mm 297mm;
            margin: 0;
        }
        .row:after {
            content: "";
            display: table;
            clear: both;
        }
        p {
            word-break: break-word;
            white-space: normal;
            margin:0;
        }
        .column {
            float: left;
            width: 50%;
            padding: 10px;
            box-sizing: border-box;
        }
"""

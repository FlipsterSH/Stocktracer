const app = Vue.createApp({
    data() {
        return {
            data: {
            "AAPL": {"price": 0, "ma50": 0, "ma100": 0, "ma150": 0, "ma200": 0, "ath": 0, "change": 0}, 
            "GOOG": {"price": 0, "ma50": 0, "ma100": 0, "ma150": 0, "ma200": 0, "ath": 0, "change": 0}, 
            "MSFT": {"price": 0, "ma50": 0, "ma100": 0, "ma150": 0, "ma200": 0, "ath": 0, "change": 0}, 
            "NDX": {"price": 0, "ma50": 0, "ma100": 0, "ma150": 0, "ma200": 0, "ath": 0, "change": 0}, 
            "SPY": {"price": 0, "ma50": 0, "ma100": 0, "ma150": 0, "ma200": 0, "ath": 0,"change": 0}, 
            "TSLA": {"price": 0, "ma50": 0, "ma100": 0, "ma150": 0, "ma200": 0, "ath": 0, "change": 0},
            "VIX": {"price": 0, "ma50": 0, "ma100": 0, "ma150": 0, "ma200": 0, "ath": 0, "change": 0},
            "AVG": 0,
            "MSG": 0
            },

            selected: "",
            update: this.update_button(),
            test: 0
        }
    },
    methods: {
        async update_button() {
            console.log("go")
            let reply = await fetch("/update");
            if (reply.status == 200) {
                result = await reply.json();
                result["NDX"] = result["^NDX"]; //her lager vi en kopi av ^NDX dict, må deretter fjerne den dict for å kunne bruke v-for i index.html
                result["VIX"] = result["^VIX"] //samme for ^VIX

                this.data = result; //setter resultatet i data i app 

                let trace = {
                    x: result.graph.daylist,
                    y: result.graph.pricelist,
                    mode: "lines"
                }

                let layout = {
                    title: "SPY",
                    //xaxis_title: "X Axis Title",
                    //yaxis_title: "Closing price"
                }

                let data = [trace]

                Plotly.newPlot('chart1', data, layout);
            }
        },

        async get_graph(graph_id) {
            let reply = await fetch("/graphinfo?graph_id=" + graph_id);
            if (reply.status == 200) {
                let result = await reply.json();
                console.log(result)

                let trace = {
                    x: result.daylist,
                    y: result.pricelist,
                    mode: "lines"
                }

                let layout = {
                    title: graph_id,
                    //xaxis_title: "X Axis Title",
                    //yaxis_title: "Closing price"
                }

                let data = [trace]

                Plotly.newPlot('chart1', data, layout);
            }        
        },
    }
});

app.mount("#app");
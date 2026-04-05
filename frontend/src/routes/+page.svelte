<script>
    import { browser, dev } from "$app/environment";
    import { onMount } from "svelte";

    let url = dev ? "http://localhost:5002" : "";
    if (!dev && browser) {
        url = location.protocol + "//" + location.host;
    }

    let downhill = 300;
    let uphill = 700;
    let length = 10000;

    let prediction = "n.a.";
    let linearPrediction = "n.a.";
    let din33466 = "n.a.";
    let sac = "n.a.";
    let history = [];

    let debounceId;

    async function fetchHistory() {
        let result = await fetch(url + "/api/history");
        history = await result.json();
    }

    async function predict() {
        let result = await fetch(
            url +
                "/api/predict?" +
                new URLSearchParams({
                    downhill: downhill,
                    uphill: uphill,
                    length: length,
                }),
            {
                method: "GET",
            },
        );
        let data = await result.json();
        console.log(data);
        prediction = data.time;
        linearPrediction = data.linear;
        din33466 = data.din33466;
        sac = data.sac;
        fetchHistory();
    }

    onMount(() => {
        predict();
        fetchHistory();
    });

    function schedulePredict() {
        if (debounceId) {
            clearTimeout(debounceId);
        }
        debounceId = setTimeout(() => {
            predict();
        }, 300);
    }
</script>

<svelte:head>
    <title>HikePlanner</title>
</svelte:head>

<div class="app-bg d-flex align-items-center justify-content-center py-5">
    <main class="container">
        <div class="row g-4 justify-content-center align-items-lg-stretch">
            
            <!-- Left Column: Input Form -->
            <div class="col-lg-5 col-md-10">
                <div class="p-4 p-lg-5 glass-card rounded-4 h-100 d-flex flex-column">
                    <div class="text-center mb-4">
                        <div class="d-inline-flex align-items-center justify-content-center bg-primary text-white rounded-circle mb-3 shadow-sm" style="width: 64px; height: 64px;">
                            <i class="bi bi-geo-alt-fill fs-2"></i>
                        </div>
                        <h1 class="display-6 fw-bold mb-2 text-white">HikePlanner</h1>
                        <p class="text-white-50 small">
                            Schätze die Gehzeit basierend auf Distanz und Höhenmetern.
                        </p>
                    </div>

                    <form class="vstack gap-4 flex-grow-1" on:submit|preventDefault={predict}>
                        <!-- Downhill -->
                        <div class="bg-black bg-opacity-25 p-3 rounded-3 border border-white border-opacity-10">
                            <label class="form-label fw-semibold text-white-50 mb-2 d-flex align-items-center">
                                <i class="bi bi-arrow-down-right-circle text-primary me-2"></i>Abwärts
                            </label>
                            <div class="row g-3 align-items-center">
                                <div class="col-8">
                                    <input type="range" class="form-range" bind:value={downhill} min="0" max="10000" step="10" on:input={schedulePredict} />
                                </div>
                                <div class="col-4">
                                    <div class="input-group input-group-sm shadow-sm">
                                        <input type="number" class="form-control text-center fw-bold" bind:value={downhill} min="0" max="10000" on:input={schedulePredict} />
                                        <span class="input-group-text">m</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Uphill -->
                        <div class="bg-black bg-opacity-25 p-3 rounded-3 border border-white border-opacity-10">
                            <label class="form-label fw-semibold text-white-50 mb-2 d-flex align-items-center">
                                <i class="bi bi-arrow-up-right-circle text-danger me-2"></i>Aufwärts
                            </label>
                            <div class="row g-3 align-items-center">
                                <div class="col-8">
                                    <input type="range" class="form-range" bind:value={uphill} min="0" max="10000" step="10" on:input={schedulePredict} />
                                </div>
                                <div class="col-4">
                                    <div class="input-group input-group-sm shadow-sm">
                                        <input type="number" class="form-control text-center fw-bold" bind:value={uphill} min="0" max="10000" on:input={schedulePredict} />
                                        <span class="input-group-text">m</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Distance -->
                        <div class="bg-black bg-opacity-25 p-3 rounded-3 border border-white border-opacity-10">
                            <label class="form-label fw-semibold text-white-50 mb-2 d-flex align-items-center">
                                <i class="bi bi-arrows-expand text-success me-2"></i>Distanz
                            </label>
                            <div class="row g-3 align-items-center">
                                <div class="col-8">
                                    <input type="range" class="form-range" bind:value={length} min="0" max="30000" step="10" on:input={schedulePredict} />
                                </div>
                                <div class="col-4">
                                    <div class="input-group input-group-sm shadow-sm">
                                        <input type="number" class="form-control text-center fw-bold" bind:value={length} min="0" max="30000" on:input={schedulePredict} />
                                        <span class="input-group-text">m</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="d-grid mt-auto pt-3">
                            <button class="btn btn-primary btn-lg rounded-pill shadow-sm fw-bold" type="submit">
                                <i class="bi bi-calculator me-2"></i>Predict
                            </button>
                        </div>
                    </form>
                </div>
            </div>

            <!-- Right Column: Results -->
            <div class="col-lg-5 col-md-10">
                <div class="p-4 p-lg-5 glass-card rounded-4 h-100 d-flex flex-column">
                    <div class="d-flex align-items-center justify-content-between mb-4 pb-2 border-bottom border-white border-opacity-10">
                        <h2 class="h4 mb-0 fw-bold text-white"><i class="bi bi-stopwatch text-primary me-2"></i>Dauer</h2>
                    </div>
                    
                    <div class="table-responsive flex-grow-1">
                        <table class="table table-hover align-middle mb-0">
                            <tbody>
                                <tr>
                                    <th scope="row" class="py-3 text-white-50 fw-normal"><i class="bi bi-robot me-2 text-info"></i>Model (GBR)</th>
                                    <td class="py-3 fw-bold text-primary fs-5">{prediction}</td>
                                </tr>
                                <tr>
                                    <th scope="row" class="py-3 text-white-50 fw-normal"><i class="bi bi-graph-up me-2 text-secondary"></i>Model (Linear)</th>
                                    <td class="py-3 fw-bold text-white">{linearPrediction}</td>
                                </tr>
                                <tr>
                                    <th scope="row" class="py-3 text-white-50 fw-normal"><i class="bi bi-file-earmark-bar-graph me-2 text-secondary"></i>DIN33466</th>
                                    <td class="py-3 fw-bold text-white">{din33466}</td>
                                </tr>
                                <tr>
                                    <th scope="row" class="py-3 text-white-50 fw-normal"><i class="bi bi-geo me-2 text-secondary"></i>SAC</th>
                                    <td class="py-3 fw-bold text-white">{sac}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="mt-4 pt-4 border-top border-white border-opacity-10 vstack gap-3">
                        <a href="{url}/api/download-prediction?downhill={downhill}&uphill={uphill}&length={length}" class="btn btn-primary rounded-pill shadow-sm" download>
                            <i class="bi bi-download me-2"></i>Download Results (.csv)
                        </a>
                    </div>
                </div>
            </div>
            
            <!-- History Section -->
            {#if history.length > 0}
            <div class="col-lg-10 mt-5">
                <div class="p-4 glass-card rounded-4">
                    <h3 class="h5 mb-4 fw-bold text-white"><i class="bi bi-clock-history text-info me-2"></i>History</h3>
                    <div class="table-responsive">
                        <table class="table table-sm table-hover align-middle small">
                            <thead class="bg-white bg-opacity-10">
                                <tr>
                                    <th class="text-white-50">Time</th>
                                    <th class="text-white-50">Inputs (D/U/L)</th>
                                    <th class="text-white-50">GBR</th>
                                    <th class="text-white-50">Linear</th>
                                    <th class="text-white-50">DIN</th>
                                    <th class="text-white-50">SAC</th>
                                </tr>
                            </thead>
                            <tbody>
                                {#each history as item}
                                <tr class="border-white border-opacity-10">
                                    <td class="text-white-50">{item.timestamp}</td>
                                    <td class="text-white">{item.inputs.downhill}m / {item.inputs.uphill}m / {item.inputs.length}m</td>
                                    <td class="fw-bold text-primary">{item.time}</td>
                                    <td class="text-white">{item.linear}</td>
                                    <td class="text-white">{item.din33466}</td>
                                    <td class="text-white">{item.sac}</td>
                                </tr>
                                {/each}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            {/if}
            
        </div>
    </main>
</div>

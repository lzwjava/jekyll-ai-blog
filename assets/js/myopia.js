/**
 * Myopia Vision Restoration Calculator
 * Based on the Natural Vision Restoration Method
 * Inspired by Todd Becker and Yin Wang's research
 */

class MyopiaCalculator {
    constructor() {
        this.measurements = [];
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Add event listeners when DOM is loaded
        document.addEventListener('DOMContentLoaded', () => {
            this.setupCalculator();
        });
    }

    setupCalculator() {
        const calculateBtn = document.getElementById('calculate-btn');
        const addMeasurementBtn = document.getElementById('add-measurement-btn');
        const clearBtn = document.getElementById('clear-btn');

        if (calculateBtn) {
            calculateBtn.addEventListener('click', () => this.calculateImprovement());
        }

        if (addMeasurementBtn) {
            addMeasurementBtn.addEventListener('click', () => this.addMeasurement());
        }

        if (clearBtn) {
            clearBtn.addEventListener('click', () => this.clearMeasurements());
        }

        // Load sample data from the blog post
        this.loadSampleData();
    }

    /**
     * Load sample data from the blog post for demonstration
     */
    loadSampleData() {
        const sampleData = [
            {
                date: '2022-03-05',
                leftMyopia: 350,
                leftAstigmatism: 225,
                rightMyopia: 575,
                rightAstigmatism: 175
            },
            {
                date: '2022-11-13',
                leftMyopia: 325,
                leftAstigmatism: 200,
                rightMyopia: 550,
                rightAstigmatism: 175
            },
            {
                date: '2023-04-20',
                leftMyopia: 300,
                leftAstigmatism: 125,
                rightMyopia: 500,
                rightAstigmatism: 125
            }
        ];

        this.measurements = sampleData;
        this.displayMeasurements();
        this.calculateImprovement();
    }

    /**
     * Add a new measurement from form inputs
     */
    addMeasurement() {
        const date = document.getElementById('measurement-date')?.value;
        const leftMyopia = parseFloat(document.getElementById('left-myopia')?.value);
        const leftAstigmatism = parseFloat(document.getElementById('left-astigmatism')?.value);
        const rightMyopia = parseFloat(document.getElementById('right-myopia')?.value);
        const rightAstigmatism = parseFloat(document.getElementById('right-astigmatism')?.value);

        if (!date || isNaN(leftMyopia) || isNaN(rightMyopia)) {
            alert('Please fill in all required fields with valid numbers');
            return;
        }

        const measurement = {
            date,
            leftMyopia,
            leftAstigmatism: leftAstigmatism || 0,
            rightMyopia,
            rightAstigmatism: rightAstigmatism || 0
        };

        this.measurements.push(measurement);
        this.measurements.sort((a, b) => new Date(a.date) - new Date(b.date));

        this.displayMeasurements();
        this.calculateImprovement();
        this.clearForm();
    }

    /**
     * Clear the input form
     */
    clearForm() {
        const inputs = ['measurement-date', 'left-myopia', 'left-astigmatism', 'right-myopia', 'right-astigmatism'];
        inputs.forEach(id => {
            const element = document.getElementById(id);
            if (element) element.value = '';
        });
    }

    /**
     * Clear all measurements
     */
    clearMeasurements() {
        if (confirm('Are you sure you want to clear all measurements?')) {
            this.measurements = [];
            this.displayMeasurements();
            this.clearResults();
        }
    }

    /**
     * Calculate improvement metrics
     */
    calculateImprovement() {
        if (this.measurements.length < 2) {
            this.displayResults({
                error: 'Need at least 2 measurements to calculate improvement'
            });
            return;
        }

        const first = this.measurements[0];
        const latest = this.measurements[this.measurements.length - 1];
        const timeSpan = this.calculateTimeSpan(first.date, latest.date);

        const improvements = {
            timeSpan,
            leftEye: {
                myopia: {
                    initial: first.leftMyopia,
                    current: latest.leftMyopia,
                    improvement: first.leftMyopia - latest.leftMyopia,
                    percentage: ((first.leftMyopia - latest.leftMyopia) / first.leftMyopia * 100).toFixed(1)
                },
                astigmatism: {
                    initial: first.leftAstigmatism,
                    current: latest.leftAstigmatism,
                    improvement: first.leftAstigmatism - latest.leftAstigmatism,
                    percentage: first.leftAstigmatism > 0 ? ((first.leftAstigmatism - latest.leftAstigmatism) / first.leftAstigmatism * 100).toFixed(1) : 0
                }
            },
            rightEye: {
                myopia: {
                    initial: first.rightMyopia,
                    current: latest.rightMyopia,
                    improvement: first.rightMyopia - latest.rightMyopia,
                    percentage: ((first.rightMyopia - latest.rightMyopia) / first.rightMyopia * 100).toFixed(1)
                },
                astigmatism: {
                    initial: first.rightAstigmatism,
                    current: latest.rightAstigmatism,
                    improvement: first.rightAstigmatism - latest.rightAstigmatism,
                    percentage: first.rightAstigmatism > 0 ? ((first.rightAstigmatism - latest.rightAstigmatism) / first.rightAstigmatism * 100).toFixed(1) : 0
                }
            }
        };

        // Calculate projected recovery time
        improvements.projections = this.calculateProjections(improvements, timeSpan);

        this.displayResults(improvements);
    }

    /**
     * Calculate time span between two dates
     */
    calculateTimeSpan(startDate, endDate) {
        const start = new Date(startDate);
        const end = new Date(endDate);
        const diffTime = Math.abs(end - start);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        const diffMonths = diffDays / 30.44; // Average days per month
        const diffYears = diffMonths / 12;

        return {
            days: diffDays,
            months: diffMonths.toFixed(1),
            years: diffYears.toFixed(1)
        };
    }

    /**
     * Calculate projections for full recovery
     */
    calculateProjections(improvements, timeSpan) {
        const projections = {};

        // Calculate monthly improvement rate
        const monthsElapsed = parseFloat(timeSpan.months);

        ['leftEye', 'rightEye'].forEach(eye => {
            projections[eye] = {};

            ['myopia', 'astigmatism'].forEach(condition => {
                const data = improvements[eye][condition];
                const monthlyImprovement = data.improvement / monthsElapsed;

                if (monthlyImprovement > 0 && data.current > 0) {
                    const monthsToRecovery = data.current / monthlyImprovement;
                    projections[eye][condition] = {
                        monthlyRate: monthlyImprovement.toFixed(1),
                        monthsToRecovery: monthsToRecovery.toFixed(1),
                        yearsToRecovery: (monthsToRecovery / 12).toFixed(1)
                    };
                } else {
                    projections[eye][condition] = {
                        monthlyRate: monthlyImprovement.toFixed(1),
                        monthsToRecovery: 'Already recovered or no improvement',
                        yearsToRecovery: 'N/A'
                    };
                }
            });
        });

        return projections;
    }

    /**
     * Calculate recommended glasses prescription
     */
    calculateGlassesPrescription(currentMyopia, reductionDegrees = 150) {
        return Math.max(0, currentMyopia - reductionDegrees);
    }

    /**
     * Display measurements table
     */
    displayMeasurements() {
        const container = document.getElementById('measurements-table');
        if (!container) return;

        if (this.measurements.length === 0) {
            container.innerHTML = '<p>No measurements recorded yet.</p>';
            return;
        }

        const table = document.createElement('table');
        table.className = 'measurement-table';
        table.innerHTML = `
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Left Myopia (°)</th>
                    <th>Left Astigmatism (°)</th>
                    <th>Right Myopia (°)</th>
                    <th>Right Astigmatism (°)</th>
                </tr>
            </thead>
            <tbody>
                ${this.measurements.map(m => `
                    <tr>
                        <td>${m.date}</td>
                        <td>${m.leftMyopia}</td>
                        <td>${m.leftAstigmatism}</td>
                        <td>${m.rightMyopia}</td>
                        <td>${m.rightAstigmatism}</td>
                    </tr>
                `).join('')}
            </tbody>
        `;

        container.innerHTML = '';
        container.appendChild(table);
    }

    /**
     * Display calculation results
     */
    displayResults(results) {
        const container = document.getElementById('results-container');
        if (!container) return;

        if (results.error) {
            container.innerHTML = `<div class="error">${results.error}</div>`;
            return;
        }

        const latest = this.measurements[this.measurements.length - 1];
        const recommendedLeft = this.calculateGlassesPrescription(latest.leftMyopia);
        const recommendedRight = this.calculateGlassesPrescription(latest.rightMyopia);

        container.innerHTML = `
            <div class="results-summary">
                <h3>Vision Improvement Analysis</h3>
                <p><strong>Time Period:</strong> ${results.timeSpan.months} months (${results.timeSpan.years} years)</p>

                <div class="eye-results">
                    <div class="left-eye">
                        <h4>Left Eye</h4>
                        <div class="improvement-stats">
                            <p><strong>Myopia:</strong> ${results.leftEye.myopia.initial}° ’ ${results.leftEye.myopia.current}°
                               (${results.leftEye.myopia.improvement > 0 ? '-' : ''}${Math.abs(results.leftEye.myopia.improvement)}°, ${results.leftEye.myopia.percentage}% improvement)</p>
                            <p><strong>Astigmatism:</strong> ${results.leftEye.astigmatism.initial}° ’ ${results.leftEye.astigmatism.current}°
                               (${results.leftEye.astigmatism.improvement > 0 ? '-' : ''}${Math.abs(results.leftEye.astigmatism.improvement)}°, ${results.leftEye.astigmatism.percentage}% improvement)</p>
                        </div>
                    </div>

                    <div class="right-eye">
                        <h4>Right Eye</h4>
                        <div class="improvement-stats">
                            <p><strong>Myopia:</strong> ${results.rightEye.myopia.initial}° ’ ${results.rightEye.myopia.current}°
                               (${results.rightEye.myopia.improvement > 0 ? '-' : ''}${Math.abs(results.rightEye.myopia.improvement)}°, ${results.rightEye.myopia.percentage}% improvement)</p>
                            <p><strong>Astigmatism:</strong> ${results.rightEye.astigmatism.initial}° ’ ${results.rightEye.astigmatism.current}°
                               (${results.rightEye.astigmatism.improvement > 0 ? '-' : ''}${Math.abs(results.rightEye.astigmatism.improvement)}°, ${results.rightEye.astigmatism.percentage}% improvement)</p>
                        </div>
                    </div>
                </div>

                <div class="projections">
                    <h4>Recovery Projections</h4>
                    <div class="projection-grid">
                        <div>
                            <strong>Left Eye Myopia:</strong><br>
                            Monthly improvement: ${results.projections.leftEye.myopia.monthlyRate}°<br>
                            Projected full recovery: ${results.projections.leftEye.myopia.yearsToRecovery} years
                        </div>
                        <div>
                            <strong>Right Eye Myopia:</strong><br>
                            Monthly improvement: ${results.projections.rightEye.myopia.monthlyRate}°<br>
                            Projected full recovery: ${results.projections.rightEye.myopia.yearsToRecovery} years
                        </div>
                    </div>
                </div>

                <div class="recommendations">
                    <h4>Recommended Glasses Prescription (150° reduction method)</h4>
                    <p><strong>Left Eye:</strong> ${recommendedLeft}° myopia, ${latest.leftAstigmatism}° astigmatism</p>
                    <p><strong>Right Eye:</strong> ${recommendedRight}° myopia, ${latest.rightAstigmatism}° astigmatism</p>
                    <p class="note"><em>Note: This is based on Todd Becker's method of reducing myopia prescription by 150°. Consult with an eye care professional before making changes.</em></p>
                </div>
            </div>
        `;
    }

    /**
     * Clear results display
     */
    clearResults() {
        const container = document.getElementById('results-container');
        if (container) {
            container.innerHTML = '';
        }
    }
}

// Initialize the calculator
const myopiaCalculator = new MyopiaCalculator();

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MyopiaCalculator;
}

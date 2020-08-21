const App = new Vue({
    el: '#mainApp',
    delimiters: ['${', '}'],

    data() {
    	return {
			errorMessage: 'testss',
			attachment: null,
			validHeaders: [
				'gender', 'name.title', 'name.first', 'name.last',
				'location.street.number', 'location.street.name',
				'location.city', 'location.country', 'phone', 'picture.large',
				'picture.medium', 'picture.thumbnail'
			],
			editedDate: '',
			customers: [],
			API_KEY: '0b309f0e29ad4ae69f282323202108',
			isFetching: false,
			errorMessage: '',
			weatherData: {}
    	}
    },

    // data() {
    // 	return {
    // 		errorMessage: 'tesssts',
    // 		attachment: null,
    // 		validHeaders: [
    // 			'gender', 'name.title', 'name.first', 'name.last',
    // 			'location.street.number', 'location.street.name',
    // 			'location.city', 'location.country', 'phone', 'picture.large',
    // 			'picture.medium', 'picture.thumbnail'
    // 		]
    // 	};
    // },

    computed: {
    	maxDate() {
    		return moment().format('YYYY-MM-DD');
    	},
    	
    	formattedDate() {
    		return moment(this.editedDate).format('MMMM DD, YYYY');
    	}
    },

    async created() {
    	console.log(this.maxDate)
    	await this.initData();
    },

    mounted: function() {
    },

    methods: {
    	async initData() {
    		await this.getAllUsers().then(response => {
    			this.customers = response;
    		});
    	},

    	async showWeather(customer) {
    		this.errorMessage = '';
    		let city = customer.location.city;
    		let data = {};
    		this.weatherData = {};
    		await this.getWeatherDetails(city).then(response => {
    			this.weatherData = response;
    		}).catch(err => {
    			this.errorMessage = err.responseJSON.error.message;
    		});
    		console.log(this.weatherData)
    	},

    	// async setAllWeather() {
    	// 	this.isFetching = true;
    	// 	for (let i = 0; i < this.customers.length; i++) {
    	// 		this.customers[i]['weather'] = await this.getWeatherDetails(
    	// 			this.customers[i].location.city);
    	// 	}
    	// 	this.isFetching = false;
    	// },

    	async getWeatherDetails(cityName) {
    		return await this.getLiveWeather(cityName);
    	},

    	handleFileInputChange() {
            let files = this.$refs.filePicker.files;
            if(!files) return;
            this.attachment = files[0];
            this.validateCSV();
        },

        validateCSV() {
            if (!this.attachment['type'].includes('csv')) {
                this.errorMessage = 'File selected is not a CSV file.';
                this.$refs.filePicker.files = null;
                this.attachment = null;
                return;
            }
            const reader = new FileReader();
            reader.onload = this.handleFileLoad;
            reader.readAsText(this.attachment);
        },

        async handleFileLoad(event) {
            let text = event.target.result;
            let jsonData = text.split(/\r?\n|\r/);
            let header = jsonData.shift().split(',');

            for (let i = 0; i < this.validHeaders.length; i++) {
                if (this.validHeaders[i] !== header[i]) {
                    this.errorMessage = 'There is a mismatch between the headers ' +
                        'of your uploaded CSV and the CSV template';
                    return;
                }
            }

            const customers = [];
            
            jsonData.forEach(item => {
            	let rowData = item.replace(/"/g, '').split(/\r?,/);
                if(rowData.length === this.validHeaders.length) {
                    let item = {};

                    this.validHeaders.forEach((header, index) => {
                    	item[header] = rowData[index];
                    });
                    customers.push(item);
                }
            });

            const payload = {
            	'customers': JSON.stringify(customers)
            }

            await this.addCustomers(payload);



        //     this.$http.get('/api/customers/')
		      // .then((response) => {
		      // 	console.log(response)
		      //   // this.articles = response.data;
		      // })
		      // .catch((err) => {
		      // })

		    
        },

        addCustomers(payload) {
        	return new Promise(function(resolve, reject) {
	    		// const formData = new FormData();
	      //       formData.append('customers', payload.customers);
	        	$.ajax({
					method: 'POST',
					url: '/apiv2/customers/create/',
					// data: JSON.stringify(payload),
					data: payload,
					dataType: 'json',
				    beforeSend: function(xhr) {
				        xhr.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'))
				    },
					success: resolve,
					error: reject
				});
			});
		 },

        getAllUsers() {
        	return new Promise(function(resolve, reject) {
	            $.ajax({
		            url: '/api/customers/',
		            method: 'GET',
		            success: resolve,
		            error: reject
		        });
	        });
        },

        getLiveWeather(cityName) {
        	let url = (
        		'http://api.weatherapi.com/v1/history.json?' +
        		`key=${this.API_KEY}&q=${cityName}&dt=${this.editedDate}`);
        	return new Promise(function(resolve, reject) {
	        	$.ajax({
		            url: url,
		            method: 'GET',
		            success: resolve,
		            error: reject
		        });
		    });
        }
    },

    filters: {
    },

    watch: {
    }

});
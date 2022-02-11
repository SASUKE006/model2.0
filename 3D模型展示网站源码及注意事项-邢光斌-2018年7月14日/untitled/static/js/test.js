	
	function music() {
			
		$('#music').addClass('music_Ani');
		$('#music').css("opacity","1");

		audio.play();		
	}
	//音乐和音乐图标播放、暂停
	function playOrPaused(audio) {
		if(audio.paused) {
			audio.play();
			$('#music').addClass('music_Ani');
		} else {
			audio.pause();
			$('#music').removeClass('music_Ani');
		}
	}	
	
	var isRoll = true;
	// once everything is loaded, we run our Three.js stuff.
	function init() {
		 
		
		//背景音乐控制
		$('#music').click(function() {
			playOrPaused(document.getElementById('audio'));
		});

		
		
		var clock = new THREE.Clock();
	
		// create a scene, that will hold all our elements such as objects, cameras and lights.
		var scene = new THREE.Scene();
	
		// create a camera, which defines where we're looking at.
		var camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 10000);
	
		//声明渲染器对象：WebGLRenderer
		var webGLRenderer = new THREE.WebGLRenderer({
			antialias: true, //是否开启反锯齿  
			precision: "highp", //着色精度选择  
			alpha: true, //是否可以设置背景色透明  
			premultipliedAlpha: false,
			stencil: false,
			preserveDrawingBuffer: true, //是否保存绘图缓冲  
			maxLights: 1 //maxLights:最大灯光数  ,
			
		});
		
        //webGLRenderer.shadowMapEnabled = true;	
		//指定渲染器的高宽（和画布框大小一致）  
		webGLRenderer.setSize(window.innerWidth, window.innerHeight);
		//追加canvas 元素到canvas3d元素中。  
		webGLRenderer.setClearColor(0xeeeeee, 1);
	
		// position and point the camera to the center of the scene
		camera.position.x = 5;
		camera.position.y = 5;
		camera.position.z = 5;
		camera.lookAt(new THREE.Vector3(0, 1, 0));
	
		var trackballControls = new THREE.TrackballControls(camera);
	
		trackballControls.rotateSpeed = 5;
		trackballControls.zoomSpeed = 0.5;
		//				trackballControls.panSpeed = 10;
		//trackballControls.noZoom = false;
		trackballControls.noPan = true;
	
		trackballControls.minDistance = 5;
		trackballControls.maxDistance = 20;
		//trackballControls.staticMoving = true;
		//trackballControls.dynamicDampingFactor=0.3;
	
	
		var ambient = new THREE.AmbientLight(0xeeeeee);
		scene.add(ambient);

	
		// LIGHTS
        // add spotlight for the shadows
        var spotLight = new THREE.SpotLight(0xffffff);
        spotLight.position.set(-40, 60, -10);
        spotLight.castShadow = true;
        scene.add(spotLight);
	
		// add the output of the renderer to the html element
		document.getElementById("WebGL-output").appendChild(webGLRenderer.domElement);
	
		
		
		// model
	
		var onProgress = function(xhr) {
			if(xhr.lengthComputable) {
				var percentComplete = xhr.loaded / xhr.total * 100;
	
				$("#text").html(Math.round(percentComplete, 2) + '%');
	
				if(Math.round(percentComplete, 2) == "100") {
					document.getElementById("text").style.opacity = "0";
					music();
				}
				console.log(Math.round(percentComplete, 2) + '% downloaded');
			}
			
			setTimeout(function () {
    			music();
 			}, 4000);
			
		};
	
		var onError = function(xhr) {};
		
		var manager = new THREE.LoadingManager();
		manager.onProgress = function (item, loaded, total) {
		console.log(item+' = '+loaded / total * 100) + '%';	
//			var percentComplete = loaded / total * 100;
//	
//			$("#text").html(Math.round(percentComplete, 2) + '%');			
			
		    //console.log(item, loaded, total);
		    
		};
		manager.onLoad = function () {
		    console.log('all items loaded');
		};
		manager.onError = function () {
		    console.log('there has been an error');
		};			
		
			
		
		// var mesh;
		// var mtlLoader = new THREE.MTLLoader();
		// mtlLoader.setPath("http://127.0.0.1:8000/"+modelPath+"/");
		// mtlLoader.load(modelName+'.mtl', function(materials) {
		// 	materials.preload();
		// 	var objLoader = new THREE.OBJLoader(manager);
		// 	objLoader.setPath("http://127.0.0.1:8000/"+modelPath+"/");
		// 	objLoader.setMaterials(materials);
		// 	objLoader.load(modelName+'.obj', function(object) {
		// 		mesh = object;
		// 		scene.add(object);
		// 	}, onProgress, onError );
        //
		// });
        var mesh;
		var mtlLoader = new THREE.MTLLoader();
		mtlLoader.setPath("http://127.0.0.1:8000/media/"+modelPath+"/");
		mtlLoader.load(modelName+'.mtl', function(materials) {
			materials.preload();
			var objLoader = new THREE.OBJLoader(manager);
			objLoader.setPath("http://127.0.0.1:8000/media/"+obj_modelPath+"/");
			objLoader.setMaterials(materials);
			objLoader.load(modelName+'.obj', function(object) {
				mesh = object;
				scene.add(object);
			}, onProgress, onError );

		});
	
		
		
		
	
		render();
	
		function render() {
			var delta = clock.getDelta();
	
			trackballControls.update(delta);
			
			if (mesh && isRoll) {
                mesh.rotation.y += 0.006;
            }
	
			// render using requestAnimationFrame
			requestAnimationFrame(render);
			webGLRenderer.render(scene, camera);
		}
		$('#print3d').click(function() {
			alert("请先通过蓝牙或WIFI连接3D打印机！");
		});		
		$('#roll').click(function() {
			isRoll=!isRoll;
		});
		//视频控制
		$('#videoIcon').click(function() {
			
			isRoll = false;
			$("#videoContent").show();
			$("#video").show();
			$("#closebtn").show();
			
			
			if(mobileType()!="IOS"){
				$("#playbtn").show();				
			}
			
			
			
			
			$("audio").each(function () { this.pause() });
			$('#music').removeClass('music_Ani');			
		});	
		$('#closebtn').click(function() {
			$("#videoContent").hide();
			
			
			$("video").each(function () { this.pause() });
			
			
			$("#video").hide();
			$("#playbtn").hide();
			
			
			isRoll = true;
			$("#closebtn").hide();
			audio.play();
			$('#music').addClass('music_Ani');
		});			
		
		
		$("#playbtn").click(function() {
			$("#playbtn").hide();
			
			$("video").each(function () { this.play() });

		});			
		
	}
	
	window.onload = init;
	
	function createSpotlight( color ) {

		var newObj = new THREE.SpotLight( color, 2 );

		newObj.castShadow = true;
		newObj.angle = 0.3;
		newObj.penumbra = 0.2;
		newObj.decay = 2;
		newObj.distance = 50;

		newObj.shadow.mapSize.width = 1024;
		newObj.shadow.mapSize.height = 1024;

		return newObj;

	}
	
	
	//手机类型
	function mobileType() {
	    var u = navigator.userAgent;
	    var type;
	    if (u.indexOf('Android') > -1 || u.indexOf('Linux') > -1) {
	        type = 'Android';
	    } else if (u.indexOf('iPhone') > -1) {
	        type = 'IOS';
	    } else if (u.indexOf('Windows Phone') > -1) {
	        type = 'WP';
	    }
	    return type;
	}
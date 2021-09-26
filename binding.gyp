{
  "targets": [
    {
      "target_name": "detection",
      "sources": [
        "src/detection.cpp",
        "src/detection.h",
        "src/deviceList.cpp"
      ],
      "include_dirs" : [
        "<!(node -e \"require('nan')\")"
      ],
      'conditions': [
        ['OS=="win"',
          {
            'sources': [
              "src/detection_win.cpp"
            ],
            'include_dirs+':
            [
              # Not needed now
            ]
          }
        ],
        ['OS=="mac"',
          {
            'sources': [
              "src/detection_mac.cpp"
            ],
            "libraries": [
              "-framework",
              "IOKit"
            ],
            'default_configuration': 'Debug',
            'configurations': {
              'Debug': {
                'defines': [ 'DEBUG', '_DEBUG' ],
              },
              'Release': {
                'defines': [ 'NDEBUG' ]
              }
            },
            'xcode_settings': {
              'MACOSX_DEPLOYMENT_TARGET': '10.9'
            }
          }
        ],
        ['OS=="linux"',
          {
            'sources': [
              "src/detection_linux.cpp"
            ],
            'link_settings': {
              'libraries': [
                '-ludev'
              ]
            }
          }
        ]
      ]
    }
  ]
}
